from utils.database import supabase


# ==================================================
# GET STAFF ITEMS
# ==================================================

def get_staff_items():

    response = (
        supabase
        .table("items")
        .select("""
            id,
            name,
            sku,
            reorder_level,
            categories (
                id,
                name
            )
        """)
        .eq("is_archived", False)
        .order("name")
        .execute()
    )

    items = []

    for item in response.data:

        category = item.get("categories") or {}

        items.append({

            "id": item["id"],

            "name": item["name"],

            "sku": item["sku"],

            "category_id": category.get("id"),

            "category_name": category.get(
                "name",
                "Uncategorized"
            ),

            "reorder_level": float(
                item["reorder_level"] or 0
            )
        })

    return items