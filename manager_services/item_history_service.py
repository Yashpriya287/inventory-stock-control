from utils.database import supabase


def get_item_history(item_id):

    # ==================================================
    # ITEM ACTIVITY HISTORY
    # ==================================================

    activity_response = (
        supabase
        .table("item_history")
        .select(
            """
            id,
            item_id,
            event_type,
            field_name,
            old_value,
            new_value,
            note,
            performed_by,
            created_at,
            users:performed_by (
                full_name,
                role
            )
            """
        )
        .eq("item_id", item_id)
        .order("created_at", desc=True)
        .execute()
    )

    # ==================================================
    # STOCK MOVEMENT HISTORY
    # ==================================================

    movement_response = (
        supabase
        .table("stock_movements")
        .select(
            """
            id,
            movement_type,
            quantity,
            location_id,
            source_location_id,
            destination_location_id,
            adjustment_reason,
            adjustment_direction,
            recorded_by,
            created_at,
            locations:location_id (
                name
            ),
            source_location:source_location_id (
                name
            ),
            destination_location:destination_location_id (
                name
            ),
            users:recorded_by (
                full_name,
                role
            )
            """
        )
        .eq("item_id", item_id)
        .order("created_at", desc=True)
        .execute()
    )

    history = []

    # ==================================================
    # ADD ITEM ACTIVITY
    # ==================================================

    for activity in activity_response.data or []:

        user = activity.get("users") or {}

        history.append({
            "history_type": "activity",
            "id": activity["id"],
            "event_type": activity["event_type"],
            "field_name": activity.get("field_name"),
            "old_value": activity.get("old_value"),
            "new_value": activity.get("new_value"),
            "note": activity.get("note"),
            "performed_by": user.get("full_name", "-"),
            "performed_by_role": user.get("role", "-"),
            "created_at": activity["created_at"]
        })

    # ==================================================
    # ADD STOCK MOVEMENTS
    # ==================================================

    for movement in movement_response.data or []:

        location = movement.get("locations") or {}
        source_location = movement.get("source_location") or {}
        destination_location = movement.get("destination_location") or {}
        user = movement.get("users") or {}

        history.append({
            "history_type": "movement",
            "id": movement["id"],
            "movement_type": movement["movement_type"],
            "quantity": movement["quantity"],

            "location_name": location.get(
                "name",
                "-"
            ),

            "source_location_name": source_location.get(
                "name",
                "-"
            ),

            "destination_location_name": destination_location.get(
                "name",
                "-"
            ),

            "adjustment_reason": movement.get(
                "adjustment_reason"
            ),

            "adjustment_direction": movement.get(
                "adjustment_direction"
            ),

            "performed_by": user.get(
                "full_name",
                "-"
            ),

            "performed_by_role": user.get(
                "role",
                "-"
            ),

            "created_at": movement["created_at"]
        })

    # ==================================================
    # SORT EVERYTHING TOGETHER
    # ==================================================

    history.sort(
        key=lambda entry: entry["created_at"],
        reverse=True
    )

    return history