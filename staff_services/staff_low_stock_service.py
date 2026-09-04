from utils.database import supabase
from staff_services.staff_movement_services import (
    get_staff_locations
)


def get_staff_low_stock_alerts(user_id):

    # ---------- GET STAFF ASSIGNED LOCATIONS ----------

    assigned_locations = get_staff_locations(user_id)

    if not assigned_locations:

        return []

    location_ids = [
        location["id"]
        for location in assigned_locations
    ]

    location_map = {
        location["id"]: location["name"]
        for location in assigned_locations
    }

    # ---------- GET STOCK FOR ASSIGNED LOCATIONS ----------

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

    # ---------- GET ACTIVE ITEMS ----------

    item_ids = list({

        row["item_id"]
        for row in stock_response.data

    })

    items_response = (
        supabase
        .table("items")
        .select("""
            id,
            name,
            reorder_level
        """)
        .eq("is_archived", False)
        .in_("id", item_ids)
        .execute()
    )

    item_map = {

        item["id"]: item
        for item in items_response.data

    }

    # ---------- BUILD LOW STOCK ALERTS ----------

    low_stock_alerts = []

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

        # Only show items at or below reorder level

        if available_stock > reorder_level:

            continue

        # ---------- STATUS ----------

        if available_stock == 0:

            status = "Out of Stock"

        elif available_stock <= (
            reorder_level * 0.5
        ):

            status = "Critical Stock"

        else:

            status = "Low Stock"

        low_stock_alerts.append({

            "Item": item["name"],

            "Location": location_map.get(
                stock["location_id"],
                "Unknown Location"
            ),

            "Available": available_stock,

            "Reorder Level": reorder_level,

            "Status": status

        })

    # ---------- SORT BY LOWEST STOCK ----------

    low_stock_alerts.sort(

        key=lambda alert: (
            alert["Available"],
            alert["Item"]
        )

    )

    return low_stock_alerts