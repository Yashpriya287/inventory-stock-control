import streamlit as st

from screens.auth.role_selection import role_selection_screen
from screens.auth.manager_auth import manager_auth_screen
from screens.auth.staff_auth import staff_auth_screen


def main():

    st.set_page_config(
        page_title="Busy - Inventory & Stock Control",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Initialize role selection
    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None


    match st.session_state["login_type"]:

        case "manager":
            manager_auth_screen()

        case "staff":
            staff_auth_screen()

        case None:
            role_selection_screen()


main()