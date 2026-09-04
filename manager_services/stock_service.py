from utils.database import supabase


def get_stock_overview(category_id=None):

    # ---------- GET STOCK ----------

    stock_response = (
        supabase
        .table("current_stock_by_location")
        .select("*")
        .execute()
    )

    # ---------- GET ITEMS ----------

    items_query = (
        supabase
        .table("items")
        .select("id, name, sku, reorder_level, category_id")
        .eq("is_archived", False)
    )

    if category_id:
        items_query = items_query.eq(
            "category_id",
            category_id
        )

    items_response = items_query.execute()

    # ---------- GET LOCATIONS ----------

    locations_response = (
        supabase
        .table("locations")
        .select("id, name")
        .eq("is_active", True)
        .execute()
    )

    # ---------- CREATE LOOKUPS ----------

    items = {
        item["id"]: item
        for item in items_response.data
    }

    locations = {
        location["id"]: location
        for location in locations_response.data
    }

    # ---------- BUILD STOCK OVERVIEW ----------

    stock_overview = []

    for stock in stock_response.data:

        item = items.get(stock["item_id"])

        location = locations.get(stock["location_id"])

        # Ignore items or locations outside filter
        if not item or not location:
            continue

        quantity_on_hand = float(
            stock["quantity_on_hand"]
        )

        stock_overview.append({

            "Item": item["name"],

            "Location": location["name"],

            "Available Stock": quantity_on_hand,

            "Status": (
                "Out of Stock"
                if quantity_on_hand <= 0
                else "Low Stock"
                if quantity_on_hand <= float(
                    item["reorder_level"]
                )
                else "In Stock"
            )
        })

    return stock_overview


def get_low_stock_alerts():

    # ---------- GET CURRENT STOCK ----------

    stock_response = ( supabase.table("current_stock_by_location") .select("*").execute())

    # ---------- GET ITEMS ----------

    items_response = ( supabase.table("items").select( "id, name, reorder_level" ).eq("is_archived", False).execute())

    # ---------- GET LOCATIONS ----------

    locations_response = ( supabase .table("locations") .select("id, name") .eq("is_active", True)  .execute() )

    # ---------- CREATE LOOKUPS ----------

    items = {
        item["id"]: item
        for item in items_response.data
    }

    locations = {
        location["id"]: location
        for location in locations_response.data
    }
    # ---------- BUILD ALERTS ----------

    low_stock_alerts = []

    for stock in stock_response.data:

        item = items.get(stock["item_id"])

        location = locations.get(stock["location_id"])

        if not item or not location:
            continue

        available_stock = float(
            stock["quantity_on_hand"]
        )

        reorder_level = float(
            item.get("reorder_level") or 0
        )

        # Skip items without a reorder level
        if reorder_level <= 0:
            continue

        # ---------- DETERMINE ALERT STATUS ----------

        if available_stock <= 0:

            status = "Out of Stock"
            priority = 1

        elif available_stock <= reorder_level * 0.5:

            status = "Critical Stock"
            priority = 2

        elif available_stock <= reorder_level*0.5:

            status = "Low Stock"
            priority = 3

        else:
            continue

        low_stock_alerts.append({

            "Item": item["name"],

            "Location": location["name"],

            "Available": available_stock,

            "Reorder Level": reorder_level,

            "Status": status,

            "Priority": priority
        })

    # ---------- SORT BY URGENCY ----------
    low_stock_alerts.sort(
        key=lambda alert: (
            alert["Priority"],
            alert["Available"]
        )
    )
    return low_stock_alerts



def get_available_stock_by_item():

    response = (
        supabase
        .table("current_stock_by_location")
        .select("item_id, quantity_on_hand")
        .execute()
    )

    available_stock_by_item = {}

    for stock in response.data:

        item_id = stock["item_id"]

        quantity = float(
            stock["quantity_on_hand"] or 0
        )

        if item_id not in available_stock_by_item:

            available_stock_by_item[item_id] = 0

        available_stock_by_item[item_id] += quantity

    return available_stock_by_item