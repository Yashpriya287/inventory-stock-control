from utils.database import supabase


# ==================================================
# GET STAFF ASSIGNED LOCATIONS
# ==================================================

def get_staff_locations(user_id):

    response = (
        supabase
        .table("user_locations")
        .select("""
            location_id,
            locations (
                id,
                name
            )
        """)
        .eq("user_id", user_id)
        .execute()
    )

    return [
        {
            "id": row["locations"]["id"],
            "name": row["locations"]["name"]
        }
        for row in response.data
        if row.get("locations")
    ]



# ==================================================
# GET STAFF LOW STOCK ITEMS
# ==================================================

def get_staff_low_stock_items(user_id):

    assigned_locations = get_staff_locations(
        user_id
    )

    location_ids = [
        location["id"]
        for location in assigned_locations
    ]

    if not location_ids:

        return []

    # ==================================================
    # LOCATION MAP
    # ==================================================

    location_map = {

        location["id"]: location["name"]

        for location in assigned_locations

    }

    # ==================================================
    # GET STOCK FOR ASSIGNED LOCATIONS
    # ==================================================

    stock_response = (

        supabase

        .table("current_stock_by_location")

        .select("""
            item_id,
            location_id,
            quantity_on_hand
        """)

        .in_(
            "location_id",
            location_ids
        )

        .execute()

    )

    # ==================================================
    # GET ITEM IDS
    # ==================================================

    item_ids = list({

        row["item_id"]

        for row in stock_response.data

    })

    if not item_ids:

        return []

    # ==================================================
    # GET ACTIVE ITEMS
    # ==================================================

    items_response = (

        supabase

        .table("items")

        .select("""
            id,
            name,
            sku,
            reorder_level
        """)

        .in_(
            "id",
            item_ids
        )

        .eq(
            "is_archived",
            False
        )

        .execute()

    )

    # ==================================================
    # CREATE ITEM MAP
    # ==================================================

    item_map = {

        item["id"]: item

        for item in items_response.data

    }

    # ==================================================
    # FIND LOW STOCK ITEMS
    # ==================================================

    low_stock_items = []

    for stock in stock_response.data:

        item = item_map.get(
            stock["item_id"]
        )

        if not item:

            continue

        available_stock = float(

            stock["quantity_on_hand"] or 0

        )

        reorder_level = float(

            item["reorder_level"] or 0

        )

        if available_stock <= reorder_level:

            low_stock_items.append({

                "id": item["id"],

                "name": item["name"],

                "sku": item["sku"],

                "location_id": stock["location_id"],

                "location_name": location_map.get(
                    stock["location_id"],
                    "-"
                ),

                "available_stock": available_stock,

                "reorder_level": reorder_level

            })

    return low_stock_items

# ==================================================
# GET STAFF RECENT ACTIVITY
# ==================================================

def get_staff_recent_activity(
    user_id,
    limit=5
):

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
        .eq("recorded_by", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data