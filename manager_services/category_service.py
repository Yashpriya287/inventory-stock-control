from utils.database import supabase
def create_category(name, description):
    data = {
        "name": name,
        "description": description
    }
    response = supabase.table("categories").insert(data).execute()
    return response.data


def get_categories():

    response = ( supabase .table("categories").select("*").order("name")   .execute())

    return response.data

def update_category(category_id, name, description):

    data = {
        "name": name,
        "description": description
    }
    response = ( supabase .table("categories").update(data).eq("id", category_id) .execute() )
    return response.data

def update_category_status(category_id, is_active):

    response = (supabase.table("categories").update({"is_active": is_active}).eq("id", category_id).execute() )

    return response.data