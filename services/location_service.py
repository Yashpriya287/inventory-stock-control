from utils.database import supabase


def create_location(name, description):
    data = {
        "name": name,
        "description": description
    }

    response = (  supabase .table("locations") .insert(data) .execute())

    return response.data


def get_locations():
    response = ( supabase .table("locations") .select("*").order("name")  .execute())

    return response.data


def update_location(location_id, name, description):

    data = {
        "name": name,
        "description": description
    }

    response = (
        supabase
        .table("locations")
        .update(data)
        .eq("id", location_id)
        .execute()
    )

    return response.data


def update_location_status(location_id, is_active):
    response = (
        supabase
        .table("locations")
        .update({
            "is_active": is_active  }) .eq("id", location_id) .execute() )

    return response.data
