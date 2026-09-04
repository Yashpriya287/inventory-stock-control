from utils.database import supabase


def create_stock_movement(
    item_id,
    movement_type,
    quantity,
    recorded_by,
    location_id=None,
    source_location_id=None,
    destination_location_id=None,
    adjustment_reason=None,
    adjustment_direction=None
):

    data = {
        "item_id": item_id,
        "movement_type": movement_type,
        "quantity": float(quantity),
        "recorded_by": recorded_by,
        "location_id": location_id,
        "source_location_id": source_location_id,
        "destination_location_id": destination_location_id,
        "adjustment_reason": adjustment_reason,
        "adjustment_direction": adjustment_direction
    }

    response = (supabase .table("stock_movements").insert(data).execute() )

    return response.data


def get_recent_stock_movements():

    response = (
        supabase
        .table("stock_movements")
        .select("""
            id,
            movement_type,
            quantity,
            adjustment_direction,
            adjustment_reason,
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
        .limit(10)
        .execute()
    )

    return response.data