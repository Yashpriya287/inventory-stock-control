import streamlit as st

from utils.layout import style_base_layout
from utils.layout import style_background_home
from utils.sidebar_layout import sidebar_base_layout
from screens.staff_pages.Dashboard import staff_dashboard_page
from screens.staff_pages.items import staff_items_page
from screens.staff_pages.stock_overview import staff_stock_overview_page
from screens.staff_pages.stock_movement import staff_stock_movements_page
from screens.staff_pages.low_stock_alert import staff_low_stock_alert_page
from screens.staff_pages.item_history import staff_item_history_page
def staff_screen():

    # ---------- PAGE STYLING ----------

    style_base_layout()
    style_background_home()
    sidebar_base_layout()

    # ---------- CURRENT USER ----------

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in first.")
        return

    # ---------- SESSION STATE ----------

    if "staff_selected_page" not in st.session_state:
        st.session_state["staff_selected_page"] = "🏠  Dashboard"

    # ---------- SIDEBAR ----------

    with st.sidebar:

        # LOGO

        st.markdown("## 📦 BUSY")
        st.caption("Inventory & Stock Control")

        st.divider()

        # ---------- USER PROFILE ----------

        st.markdown(
            f"""
            <div class="profile-name">
                👤 {current_user["full_name"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="manager-role">
                Warehouse Staff
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # ---------- NAVIGATION ----------

        st.markdown(
            '<div class="nav-title">NAVIGATION</div>',
            unsafe_allow_html=True
        )

        selected_page = st.radio(
            "Navigation",
            [
                "🏠  Dashboard",
                "📦  Items",
                "📊  Stock Overview",
                "↔️  Stock Movements",
                "🔔  Low Stock Alerts",
                "↩️  Item History"
            ],
            key="staff_selected_page",
            label_visibility="collapsed"
        )

        st.divider()

        # ---------- LOGOUT ----------

        if st.button(
            "🚪   Logout",
            use_container_width=True
        ):
            st.session_state.clear()
            st.rerun()

        # ---------- FOOTER ----------

        st.markdown(
            """
            <div class="sidebar-footer">
                © 2026 BUSY System<br>
                All rights reserved.
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------- PAGE NAME ----------

    page_name = selected_page.split("  ")[-1]

    # ---------- PAGE ROUTING ----------

    if page_name == "Dashboard":
        staff_dashboard_page()

    elif page_name == "Items":

        staff_items_page()

    elif page_name == "Stock Overview":

        staff_stock_overview_page()

    elif page_name == "Stock Movements":

        staff_stock_movements_page()

    elif page_name == "Low Stock Alerts":

        staff_low_stock_alert_page()

    elif page_name == "Item History":

        staff_item_history_page()