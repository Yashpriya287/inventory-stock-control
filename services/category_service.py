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

