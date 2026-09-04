from utils.database import supabase


# ---------- GET STAFF USERS ----------

def get_staff_users():

    response = (
        supabase
        .table("users")
        .select(
            "id, full_name, email, role, is_active"
        )
        .eq("role", "staff")
        .order("full_name")
        .execute()
    )

    return response.data


# ---------- UPDATE STAFF STATUS ----------

def update_staff_status(user_id, is_active):

    response = (
        supabase
        .table("users")
        .update({
            "is_active": is_active
        })
        .eq("id", user_id)
        .eq("role", "staff")
        .execute()
    )

    return response.data


# ---------- GET ACTIVE LOCATIONS ----------

def get_active_locations():

    response = (
        supabase
        .table("locations")
        .select(
            "id, name"
        )
        .eq("is_active", True)
        .order("name")
        .execute()
    )

    return response.data


# ---------- GET STAFF ASSIGNED LOCATIONS ----------

def get_staff_locations(user_id):

    response = (
        supabase
        .table("user_locations")
        .select(
            "location_id"
        )
        .eq("user_id", user_id)
        .execute()
    )

    return [
        assignment["location_id"]
        for assignment in response.data
    ]


# ---------- UPDATE STAFF LOCATION ASSIGNMENTS ----------

def update_staff_locations(user_id, location_ids):

    # Remove existing assignments
    (
        supabase
        .table("user_locations")
        .delete()
        .eq("user_id", user_id)
        .execute()
    )

    # If no locations are selected,
    # only the old assignments need to be removed
    if not location_ids:
        return

    # Create new assignments
    assignments = [
        {
            "user_id": user_id,
            "location_id": location_id
        }
        for location_id in location_ids
    ]

    response = (
        supabase
        .table("user_locations")
        .insert(assignments)
        .execute()
    )

    return response.data




