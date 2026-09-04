from utils.database import supabase

#  GET STAFF ASSIGNED LOCATIONS
def get_staff_locations(user_id):
    response = (
        supabase
        .table("user_locations")
        .select("""location_id,locations (id,name)""").eq("user_id", user_id).execute() )
    return [
        {
            "id": row["locations"]["id"],
            "name": row["locations"]["name"]
        }
        for row in response.data
        if row.get("locations")]

# GET ACTIVE ITEMS 

def get_active_items():
    response = (
        supabase
        .table("items").select("""
            id,
            name,
            sku,unit_of_measure""").eq("is_archived", False).order("name").execute() )

    return response.data


#  GET ITEMS WITH STOCK AT LOCATION

def get_items_with_stock(location_id):
    stock_response = (
        supabase
        .table("current_stock_by_location")
        .select("""
            item_id,
            quantity_on_hand
        """)
        .eq("location_id", location_id)
        .execute()
    )
    stock_map = {
        row["item_id"]: float(row["quantity_on_hand"])
        for row in stock_response.data
        if float(row["quantity_on_hand"]) > 0
    }

    if not stock_map:
        return []
    items_response = (
        supabase
        .table("items")
        .select("""
            id,
            name,
            sku,
            unit_of_measure
        """)
        .eq("is_archived", False)
        .in_("id", list(stock_map.keys()))
        .order("name")
        .execute()
    )

    items = []
    for item in items_response.data:
        item["available_stock"] = stock_map[item["id"]]
        items.append(item)
    return items


#  CHECK STAFF LOCATION ACCESS 

def is_staff_assigned_to_location(user_id, location_id):

    response = (
        supabase
        .table("user_locations")
        .select("location_id")
        .eq("user_id", user_id)
        .eq("location_id", location_id)
        .execute()
    )

    return len(response.data) > 0


#  GET CURRENT STOCK 

def get_item_stock_at_location(item_id, location_id):

    response = (
        supabase
        .table("current_stock_by_location")
        .select("quantity_on_hand")
        .eq("item_id", item_id)
        .eq("location_id", location_id)
        .execute()
    )

    if not response.data:
        return 0

    return float(response.data[0]["quantity_on_hand"])


#  RECORD STAFF MOVEMENT 

def create_staff_stock_movement(user_id,item_id,movement_type,quantity,location_id=None,source_location_id=None,destination_location_id=None):
    movement_type = movement_type.lower()
    #  VALID MOVEMENT TYPES 
    if movement_type not in ["receipt","issue", "transfer"]:
        raise ValueError("Staff can only record receipts, issues and transfers." )
    quantity = float(quantity)
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")
    #  CHECK ITEM 
    item_response = (
        supabase
        .table("items")
        .select("id")
        .eq("id", item_id)
        .eq("is_archived", False)
        .execute()
    )

    if not item_response.data:

        raise ValueError(
            "This item is unavailable or archived."
        )

    # ---------- RECEIPT / ISSUE ----------

    if movement_type in ["receipt", "issue"]:

        if not location_id:

            raise ValueError(
                "Please select a location."
            )

        if not is_staff_assigned_to_location(
            user_id,
            location_id
        ):

            raise ValueError(
                "You are not assigned to this location."
            )

        # ---------- CHECK ISSUE STOCK ----------

        if movement_type == "issue":

            current_stock = get_item_stock_at_location(
                item_id,
                location_id
            )

            if quantity > current_stock:

                raise ValueError(
                    "Insufficient stock at this location."
                )

        data = {
            "item_id": item_id,
            "movement_type": movement_type,
            "quantity": quantity,
            "location_id": location_id,
            "recorded_by": user_id
        }

    # ---------- TRANSFER ----------

    else:

        if (
            not source_location_id
            or not destination_location_id
        ):

            raise ValueError(
                "Please select both locations."
            )

        if source_location_id == destination_location_id:

            raise ValueError(
                "Source and destination locations must be different."
            )

        # Staff must be assigned to BOTH locations

        if not is_staff_assigned_to_location(
            user_id,
            source_location_id
        ):

            raise ValueError(
                "You are not assigned to the source location."
            )

        if not is_staff_assigned_to_location(
            user_id,
            destination_location_id
        ):

            raise ValueError(
                "You are not assigned to the destination location."
            )

        current_stock = get_item_stock_at_location(
            item_id,
            source_location_id
        )

        if quantity > current_stock:

            raise ValueError(
                "Insufficient stock at the source location."
            )

        data = {
            "item_id": item_id,
            "movement_type": "transfer",
            "quantity": quantity,
            "source_location_id": source_location_id,
            "destination_location_id": destination_location_id,
            "recorded_by": user_id
        }

    # ---------- CREATE MOVEMENT ----------

    response = (
        supabase
        .table("stock_movements")
        .insert(data)
        .execute()
    )

    return response.data


# ---------- GET STAFF RECENT MOVEMENTS ----------

def get_staff_recent_movements(user_id):

    # Get staff assigned locations

    assigned_locations = get_staff_locations(user_id)

    location_ids = [
        location["id"]
        for location in assigned_locations
    ]

    if not location_ids:
        return []

    response = (
        supabase
        .table("stock_movements")
        .select("""
            id,
            movement_type,
            quantity,
            created_at,
            items (
                name,
                sku
            ),
            locations!stock_movements_location_id_fkey (
                name
            ),
            source_location:locations!stock_movements_source_location_id_fkey (
                name
            ),
            destination_location:locations!stock_movements_destination_location_id_fkey (
                name
            )
        """)
        .order("created_at", desc=True)
        .limit(50)
        .execute()
    )

    # Filter movements for assigned locations

    recent_movements = []

    for movement in response.data:

        movement_type = movement["movement_type"].lower()

        if movement_type == "transfer":

            source = movement.get("source_location") or {}
            destination = movement.get("destination_location") or {}

            source_name = source.get("name")
            destination_name = destination.get("name")

            assigned_names = [
                location["name"]
                for location in assigned_locations
            ]

            if (
                source_name in assigned_names
                or destination_name in assigned_names
            ):
                recent_movements.append(movement)

        else:

            location = movement.get("locations") or {}

            location_name = location.get("name")

            assigned_names = [
                location["name"]
                for location in assigned_locations
            ]

            if location_name in assigned_names:
                recent_movements.append(movement)

    return recent_movements[:10]