import streamlit as st

from utils.database import supabase
from manager_services.stock_movement_service import get_recent_stock_movements
from manager_services.stock_service import get_low_stock_alerts


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

    def handle_quick_action(page, action):
        st.session_state["selected_page"] = page
        st.session_state["dashboard_action"] = action

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

   # ---------- QUICK ACTIONS ----------

    st.subheader("Quick Actions")

    action_col1, action_col2, action_col3, action_col4 = st.columns(4)

    with action_col1:

        st.button(
            "➕ Add Item",
            use_container_width=True,
            on_click=handle_quick_action,
            args=(
                "📦  Items",
                "add_item"
            )
        )


    with action_col2:
        if st.button("📥 Receive Stock", use_container_width=True):
            st.session_state["dashboard_action"] = "Stock Movements"
            st.session_state["stock_movement_action"] = "Receive"
            st.rerun()


    with action_col3:
        if st.button("↔️ Transfer Stock", use_container_width=True):
            st.session_state["dashboard_action"] = "Stock Movements"
            st.session_state["stock_movement_action"] = "Transfer"
            st.rerun()


    with action_col4:

        st.button(
            "👥 Manage Staff",
            use_container_width=True,
            on_click=handle_quick_action,
            args=(
                "👥  Users",
                "add_staff"
            )
        )

    st.divider()
    # SECOND SECTION

    left_col, right_col = st.columns([1.2, 1],gap="large")

    # ---------- RECENT ACTIVITY ----------

    with left_col:

        st.subheader("Recent Activity")

        recent_movements = get_recent_stock_movements()[:3]

        if recent_movements:

            for movement in recent_movements:

                item_name = movement["items"]["name"]

                movement_type = movement["movement_type"].lower()

                if movement_type == "transfer":

                    from_location = (
                        movement.get("source_location") or {}
                    ).get("name", "Unknown")

                    to_location = (
                        movement.get("destination_location") or {}
                    ).get("name", "Unknown")

                    location = f"{from_location} → {to_location}"

                else:

                    location = (
                        movement.get("locations") or {}
                    ).get("name", "Unknown Location")

                st.info(
                    f"**{movement['movement_type'].title()}:** "
                    f"{movement['quantity']} {item_name} → "
                    f"**{location}**"
                )

        else:
            st.info("No recent activity.")


    with right_col:

        st.subheader("Low Stock Alerts")

        low_stock_alerts = get_low_stock_alerts()

        if low_stock_alerts:

            for alert in low_stock_alerts:

                st.warning(
                    f"⚠ **{alert['Item']}** — "
                    f"{alert['Location']}"
                )

        else:
            st.success("No low stock alerts.")

    