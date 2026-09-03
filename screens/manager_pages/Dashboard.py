import streamlit as st

from utils.database import supabase


def get_dashboard_data():

    total_items = (supabase.table("items") .select("id", count="exact") .eq("is_archived", False) .execute() )

    total_categories = ( supabase.table("categories").select("id", count="exact").execute())

    total_locations = ( supabase.table("locations") .select("id", count="exact").eq("is_active", True).execute())

    total_staff = ( supabase .table("users") .select("id", count="exact").eq("role", "staff") .eq("is_active", True).execute())

    return {
        "items": total_items.count or 0,
        "categories": total_categories.count or 0,
        "locations": total_locations.count or 0,
        "staff": total_staff.count or 0
    }


def dashboard_screen():

    current_user = st.session_state.get("user")

    data = get_dashboard_data()

    # PAGE HEADER

    st.title("Dashboard")

    if current_user:
        st.write(f"Welcome back, **{current_user['full_name']}** 👋")

    st.write( "Here's an overview of your inventory workspace.")

    st.space("small")

    # METRICS

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(  "📦 Total Items",  data["items"])
    with col2:
        st.metric(  "🏷️ Categories",  data["categories"] )

    with col3:
        st.metric("📍 Active Locations", data["locations"] )

    with col4:
        st.metric("👥 Active Staff",data["staff"])

    st.divider()

    # QUICK ACTIONS

    st.subheader("Quick Actions")

    action_col1, action_col2, action_col3, action_col4 = st.columns(4) 

    with action_col1:

        if st.button( "➕ Add Item", use_container_width=True ):
            st.session_state["dashboard_action"] = "Items"

    with action_col2:

        if st.button( "📥 Receive Stock", use_container_width=True):
            st.session_state["dashboard_action"] = "Stock Movements"

    with action_col3:

        if st.button( "↔️ Transfer Stock", use_container_width=True ):
            st.session_state["dashboard_action"] = "Stock Movements"

    with action_col4:

        if st.button( "➕ Add Staff", use_container_width=True):
            st.session_state["dashboard_action"] = "Users"


    st.divider()
    # SECOND SECTION

    left_col, right_col = st.columns([1.2, 1],  gap="large")

    with left_col:

        st.subheader("Recent Activity")

        st.info(  "Recent stock movements will appear here.")

    with right_col:

        st.subheader("Low Stock Alerts")

        st.success( "No low stock alerts." )