from utils.database import supabase


def get_item_history(item_id):

    response = (
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
                full_name
            )
            """
        )
        .eq("item_id", item_id)
        .order("created_at", desc=True)
        .execute()
    )

    history = []

    for movement in response.data:

        location = movement.get("locations") or {}
        source_location = movement.get("source_location") or {}
        destination_location = movement.get("destination_location") or {}
        user = movement.get("users") or {}

        history.append({
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

            "created_at": movement["created_at"]
        })

    return history