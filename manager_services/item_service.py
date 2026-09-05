from utils.database import supabase


def create_item(
    sku,
    name,
    description,
    unit_of_measure,
    reorder_level,
    category_id,
    performed_by
):
    data = {
        "sku": sku,
        "name": name,
        "description": description or None,
        "unit_of_measure": unit_of_measure,
        "reorder_level": float(reorder_level),
        "category_id": category_id
    }

    response = (
        supabase
        .table("items")
        .insert(data)
        .execute()
    )

    created_item = response.data[0]

    # Record item creation in immutable history
    supabase.table("item_history").insert({
        "item_id": created_item["id"],
        "event_type": "created",
        "performed_by": performed_by
    }).execute()

    return response.data
def get_items():

    response = (
        supabase
        .table("items")
        .select("""
            *,
            categories (
                id,
                name
            )
        """)
        .execute()
    )

    return response.data

def get_manager_items(
    search="",
    category_id=None,
    location_id=None,
    show_archived=False,
    at_or_below_reorder=False,
    sort_by="name",
    sort_desc=False,
    page=1,
    page_size=10
):
    """
    Get manager items with filtering,
    sorting and pagination.
    """

    # --------------------------------------------------
    # GET ITEMS
    # --------------------------------------------------

    query = (
        supabase
        .table("items")
        .select(
            """
            id,
            sku,
            name,
            description,
            unit_of_measure,
            reorder_level,
            category_id,
            is_archived,
            categories (
                id,
                name
            )
            """,
            count="exact"
        )
    )

    # --------------------------------------------------
    # ARCHIVED FILTER
    # --------------------------------------------------

    if not show_archived:
        query = query.eq("is_archived", False)

    # --------------------------------------------------
    # CATEGORY FILTER
    # --------------------------------------------------

    if category_id:
        query = query.eq("category_id", category_id)

    # --------------------------------------------------
    # SEARCH FILTER
    # --------------------------------------------------

    if search:
        search = search.strip()

        query = query.or_(
            f"name.ilike.%{search}%,sku.ilike.%{search}%"
        )

    # --------------------------------------------------
    # SORTING
    # --------------------------------------------------

    if sort_by == "name":
        query = query.order(
            "name",
            desc=sort_desc
        )

    elif sort_by == "reorder_level":
        query = query.order(
            "reorder_level",
            desc=sort_desc
        )

    else:
        query = query.order(
            "name",
            desc=False
        )

    # --------------------------------------------------
    # PAGINATION
    # --------------------------------------------------

    page = max(1, int(page))
    page_size = max(1, int(page_size))

    start = (page - 1) * page_size
    end = start + page_size - 1

    query = query.range(start, end)

    response = query.execute()

    items = response.data or []

    # --------------------------------------------------
    # LOCATION / STOCK FILTER
    # --------------------------------------------------

    if location_id or at_or_below_reorder or sort_by == "on_hand":

        # --------------------------------------------------
        # GET STOCK FOR DISPLAYED ITEMS
        # --------------------------------------------------

        item_ids = [
            item["id"]
            for item in items
        ]

        stock_map = {}

        if item_ids:

            stock_query = (
                supabase
                .table("current_stock_by_location")
                .select(
                    "item_id, location_id, quantity_on_hand"
                )
                .in_("item_id", item_ids)
            )

            # If a specific location is selected,
            # only get stock from that location.
            if location_id:
                stock_query = stock_query.eq(
                    "location_id",
                    location_id
                )

            stock_response = stock_query.execute()

            # --------------------------------------------------
            # SUM STOCK
            # --------------------------------------------------

            for stock in stock_response.data or []:

                item_id = stock["item_id"]

                quantity = float(
                    stock["quantity_on_hand"] or 0
                )

                # This automatically:
                # - sums all locations when location_id is None
                # - uses only the selected location otherwise
                stock_map[item_id] = (
                    stock_map.get(item_id, 0)
                    + quantity
                )


        # --------------------------------------------------
        # ADD STOCK TO ITEMS
        # --------------------------------------------------

        for item in items:

            item["quantity_on_hand"] = stock_map.get(
                item["id"],
                0
            )


        # --------------------------------------------------
        # AT / BELOW REORDER FILTER
        # --------------------------------------------------

        if at_or_below_reorder:

            items = [
                item
                for item in items
                if item["quantity_on_hand"]
                <= float(item["reorder_level"] or 0)
            ]


        # --------------------------------------------------
        # SORT BY STOCK
        # --------------------------------------------------

        if sort_by == "on_hand":

            items.sort(
                key=lambda item: item["quantity_on_hand"],
                reverse=sort_desc
            )

    else:

        for item in items:
            item["quantity_on_hand"] = 0

    return {
        "items": items,
        "total_count": response.count or 0
    }


def update_item(
    item_id,
    sku,
    name,
    reorder_level,
    category_id,
    performed_by
):

    # Get current item before updating
    current_response = (
        supabase
        .table("items")
        .select(
            """
            id,
            sku,
            name,
            reorder_level,
            category_id,
            categories (
                id,
                name
            )
            """
        )
        .eq("id", item_id)
        .single()
        .execute()
    )

    current_item = current_response.data

    data = {
        "sku": sku,
        "name": name,
        "reorder_level": float(reorder_level),
        "category_id": category_id
    }

    response = (
        supabase
        .table("items")
        .update(data)
        .eq("id", item_id)
        .execute()
    )

    # ==================================================
    # NAME CHANGE
    # ==================================================

    if current_item["name"] != name:

        supabase.table("item_history").insert({
            "item_id": item_id,
            "event_type": "field_changed",
            "field_name": "name",
            "old_value": current_item["name"],
            "new_value": name,
            "performed_by": performed_by
        }).execute()

    # ==================================================
    # CATEGORY CHANGE
    # ==================================================

    if current_item["category_id"] != category_id:

        old_category = (
            current_item.get("categories") or {}
        ).get("name", "-")

        new_category_response = (
            supabase
            .table("categories")
            .select("name")
            .eq("id", category_id)
            .single()
            .execute()
        )

        new_category = (
            new_category_response.data or {}
        ).get("name", "-")

        supabase.table("item_history").insert({
            "item_id": item_id,
            "event_type": "field_changed",
            "field_name": "category",
            "old_value": old_category,
            "new_value": new_category,
            "performed_by": performed_by
        }).execute()

    # ==================================================
    # REORDER LEVEL CHANGE
    # ==================================================

    old_reorder_level = float(
        current_item["reorder_level"] or 0
    )

    new_reorder_level = float(
        reorder_level or 0
    )

    if old_reorder_level != new_reorder_level:

        supabase.table("item_history").insert({
            "item_id": item_id,
            "event_type": "field_changed",
            "field_name": "reorder_level",
            "old_value": old_reorder_level,
            "new_value": new_reorder_level,
            "performed_by": performed_by
        }).execute()

    return response.data


def update_item_status(item_id, is_archived):

    response = (
        supabase
        .table("items")
        .update({
            "is_archived": is_archived
        })
        .eq("id", item_id)
        .execute()
    )

    return response.data