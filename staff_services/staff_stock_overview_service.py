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
# GET STAFF STOCK OVERVIEW
# ==================================================

def get_staff_stock_overview(user_id):

    assigned_locations = get_staff_locations(user_id)

    location_ids = [
        location["id"]
        for location in assigned_locations
    ]

    if not location_ids:
        return []

    # ---------- GET STOCK FROM VIEW ----------

    stock_response = (
        supabase
        .table("current_stock_by_location")
        .select("""
            item_id,
            location_id,
            quantity_on_hand
        """)
        .in_("location_id", location_ids)
        .execute()
    )

    if not stock_response.data:
        return []

    # ---------- GET ITEM IDS ----------

    item_ids = list({
        row["item_id"]
        for row in stock_response.data
    })

    # ---------- GET ITEMS SEPARATELY ----------

    items_response = (
        supabase
        .table("items")
        .select("""
            id,
            name,
            sku,
            reorder_level,
            unit_of_measure,
            is_archived
        """)
        .in_("id", item_ids)
        .eq("is_archived", False)
        .execute()
    )

    item_map = {
        item["id"]: item
        for item in items_response.data
    }

    # ---------- LOCATION MAP ----------

    location_map = {
        location["id"]: location["name"]
        for location in assigned_locations
    }

    # ---------- COMBINE STOCK + ITEMS ----------

    overview = []

    for stock in stock_response.data:

        item = item_map.get(stock["item_id"])

        if not item:
            continue

        quantity = float(
            stock["quantity_on_hand"] or 0
        )

        reorder_level = float(
            item["reorder_level"] or 0
        )

        # ---------- STATUS ----------

        if quantity <= 0:

            status = "Out of Stock"

        elif quantity <= reorder_level:

            status = "Low Stock"

        else:

            status = "In Stock"

        overview.append({

            "item_id": item["id"],

            "item_name": item["name"],

            "sku": item["sku"],

            "unit_of_measure": item[
                "unit_of_measure"
            ],

            "location_id": stock["location_id"],

            "location_name": location_map.get(
                stock["location_id"],
                "-"
            ),

            "available_stock": quantity,

            "reorder_level": reorder_level,

            "status": status
        })

    return overview