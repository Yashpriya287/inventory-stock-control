from utils.database import supabase

from staff_services.staff_movement_services import (
    get_staff_locations
)


# ---------- GET STAFF ITEM HISTORY ----------

def get_staff_item_history(
    user_id,
    item_id
):

    # ---------- GET STAFF ASSIGNED LOCATIONS ----------

    assigned_locations = get_staff_locations(
        user_id
    )

    location_ids = [
        location["id"]
        for location in assigned_locations
    ]

    # Staff has no assigned locations

    if not location_ids:

        return []

    # ---------- GET ITEM MOVEMENTS ----------

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

    # ---------- FILTER HISTORY ----------

    for movement in response.data:

        movement_type = movement[
            "movement_type"
        ].lower()

        # ---------- RECEIPT / ISSUE ----------

        if movement_type in [
            "receipt",
            "issue"
        ]:

            if (
                movement.get("location_id")
                not in location_ids
            ):

                continue

        # ---------- TRANSFER ----------

        elif movement_type == "transfer":

            source_location_id = movement.get(
                "source_location_id"
            )

            destination_location_id = movement.get(
                "destination_location_id"
            )

            # Show if either location
            # belongs to the staff member

            if (
                source_location_id not in location_ids
                and destination_location_id
                not in location_ids
            ):

                continue

        # ---------- LOCATION DATA ----------

        location = (
            movement.get("locations")
            or {}
        )

        source_location = (
            movement.get("source_location")
            or {}
        )

        destination_location = (
            movement.get("destination_location")
            or {}
        )

        user = (
            movement.get("users")
            or {}
        )

        # ---------- ADD TO HISTORY ----------

        history.append({

            "id": movement["id"],

            "movement_type": movement[
                "movement_type"
            ],

            "quantity": movement[
                "quantity"
            ],

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

            "performed_by": user.get(
                    "full_name",
                    "-"
                ),

                "user_role": user.get(
                    "role",
                    "-"
                ),

            "created_at": movement[
                "created_at"
            ]

        })

    return history