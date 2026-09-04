from utils.database import supabase


def create_item( sku, name, description,unit_of_measure,reorder_level, category_id):
    data = {
        "sku": sku,
        "name": name,
        "description": description or None,
        "unit_of_measure": unit_of_measure,
        "reorder_level": float(reorder_level),
        "category_id": category_id
    }

    response = ( supabase.table("items") .insert(data).execute())
    return response.data


def get_items():

    response = ( supabase.table("items") .select(""" *, categories ( id, name )  """) .execute() )

    return response.data


def update_item(item_id,sku,name,reorder_level,category_id):
    data = {
        "sku": sku,
        "name": name,
        "reorder_level": float(reorder_level),
        "category_id": category_id
    }
    response = (supabase.table("items").update(data).eq("id", item_id).execute())

    return response.data


def update_item_status(item_id, is_archived):
    response = (supabase.table("items").update({"is_archived": is_archived}).eq("id", item_id) .execute())

    return response.data