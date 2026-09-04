import streamlit as st

from utils.layout import style_base_layout
from utils.layout import style_background_home
from utils.sidebar_layout import sidebar_base_layout
from screens.manager_pages.Dashboard import dashboard_screen
from screens.manager_pages.Items import items_page
from screens.manager_pages.category import category_page
from screens.manager_pages.Locations import locations_page
from screens.manager_pages.stock_overview import stock_overview_page
from screens.manager_pages.Stock_Movements import stock_movement_page
from screens.manager_pages.Alerts import low_stock_alerts_page
from screens.manager_pages.item_history import item_history_page
from screens.manager_pages.user import users_page
def manager_screen():
    style_base_layout()
    style_background_home()
    sidebar_base_layout()

    

    current_user = st.session_state.get("user")

    if not current_user:
        st.warning("Please log in first.")
        return

    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "🏠  Dashboard"

    # ---------- DASHBOARD QUICK ACTION ----------

    if st.session_state.get("dashboard_action"):

        action = st.session_state["dashboard_action"]

        if action == "Items":
            st.session_state["selected_page"] = "📦  Items"

        elif action == "Stock Movements":
            st.session_state["selected_page"] = "↔️  Stock Movements"

        elif action == "Users":
            st.session_state["selected_page"] = "👥  Users"

        # Clear the dashboard action after changing the page
        st.session_state["dashboard_action"] = None
        

    with st.sidebar:

    # LOGO
        st.markdown("## 📦 BUSY")
        st.caption("Inventory & Stock Control")

        st.divider()


        # USER PROFILE

        st.markdown(
                f'<div class="profile-name">'
                f'👤{current_user["full_name"]}'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown(
                '<div class="manager-role">'
                'Manager'
                '</div>',
                unsafe_allow_html=True
            )

        st.divider()


        # NAVIGATION

        st.markdown(
            '<div class="nav-title">NAVIGATION</div>',
            unsafe_allow_html=True
        )

        selected_page = st.radio(
            "Navigation",
            [
                "🏠  Dashboard",
                "📦  Items",
                "🏷️  Categories",
                "📍  Locations",
                "📊  Stock Overview",
                "↔️  Stock Movements",
                "👥  Users",
                "🔔  Low Stock Alerts",
                "↩️  Item History"
            ],
            key="selected_page",
            label_visibility="collapsed"
        )

        st.divider()


        # LOGOUT

        if st.button(
            "🚪   Logout",
            use_container_width=True
        ):
            st.session_state.clear()
            st.rerun()


        # FOOTER

        st.markdown(
            """
            <div class="sidebar-footer">
                © 2026 BUSY System<br>
                All rights reserved.
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------
    # REMOVE ICON FROM SELECTED PAGE
    # --------------------------------

    page_name = selected_page.split("  ")[-1]


    # --------------------------------
    # MAIN PAGE
    # --------------------------------

    if page_name == "Dashboard":

        dashboard_screen()


    elif page_name == "Items":

        items_page()


    elif page_name == "Categories":

        category_page()


    elif page_name == "Locations":

        locations_page()


    elif page_name == "Stock Overview":

        stock_overview_page()


    elif page_name == "Stock Movements":

        stock_movement_page()


    elif page_name == "Users":

        users_page()


    elif page_name == "Low Stock Alerts":

        low_stock_alerts_page()


    elif page_name == "Item History":

        item_history_page()

