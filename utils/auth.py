import bcrypt

from utils.database import supabase


def hash_password(password):
    return bcrypt.hashpw( password.encode(),bcrypt.gensalt()).decode()


def check_password(password, password_hash):
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def check_email_exists(email):
    response = ( supabase .table("users").select("email") .eq("email", email) .execute() )
    return len(response.data) > 0


def create_manager(full_name, email, password):

    password_hash = hash_password(password)
    data = { "email": email, "password_hash": password_hash, "full_name": full_name, "role": "manager"}
    response = (supabase.table("users").insert(data).execute())

    return response.data


def manager_login(email, password):

    response = ( supabase  .table("users").select("*") .eq("email", email)  .eq("role", "manager").execute())
    if response.data:
        manager = response.data[0]
        if not manager["is_active"]:
            return None
        if check_password(password, manager["password_hash"]):
            return manager

    return None

def create_staff(full_name, email, password):
    password_hash = hash_password(password)
    data = { "email": email,"password_hash": password_hash,"full_name": full_name, "role": "staff"}
    response = (supabase .table("users").insert(data).execute() )
    return response.data


def staff_login(email, password):

    response = ( supabase .table("users").select("*") .eq("email", email).eq("role", "staff") .execute())
    if response.data:
        staff = response.data[0]
        if not staff["is_active"]:
            return None
        if check_password( password, staff["password_hash"]):
            return staff
    return None