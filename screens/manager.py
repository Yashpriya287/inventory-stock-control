import streamlit as st

from utils.layout import style_base_layout
from utils.layout import style_background_home
from utils.sidebar_layout import sidebar_base_layout
from screens.manager_pages.Dashboard import dashboard_screen
from screens.manager_pages.Items import items_page
from screens.manager_pages.category import category_page
def manager_screen():
    style_base_layout()
    style_background_home()
    sidebar_base_layout()

    

    current_user = st.session_state.get("user")

    if not current_user:
        st.warning("Please log in first.")
        return

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

        st.title("Locations")
        st.write("Manage inventory locations here.")


    elif page_name == "Stock Overview":

        st.title("Stock Overview")
        st.write(
            "View current stock across all locations."
        )


    elif page_name == "Stock Movements":

        st.title("Stock Movements")
        st.write(
            "Manage receipts, issues, transfers and adjustments."
        )


    elif page_name == "Users":

        st.title("Users")
        st.write(
            "Manage staff users and their access."
        )


    elif page_name == "Low Stock Alerts":

        st.title("Low Stock Alerts")
        st.write(
            "View and manage low stock alerts."
        )


    elif page_name == "Item History":

        st.title("Item History")
        st.write(
            "View complete item activity history."
        )

