import streamlit as st

from utils.layout import (
    style_base_layout,
    style_background_home
)
from utils.header import render_header
from utils.footer import render_footer
from utils.auth import (check_email_exists,create_manager,manager_login)
from screens.manager import manager_screen
def manager_auth_screen():
    st.markdown("""
        <style>

        /* Hide Streamlit password visibility button */
        div[data-testid="stTextInput"] button {
            display: none !important;
        }

        /* Remove unnecessary right-side space */
        div[data-testid="stTextInput"] input {
            padding-right: 1rem !important;
        }
        </style>
        """, unsafe_allow_html=True)




    style_base_layout()
    style_background_home()

    st.markdown("""
        <style>

        .block-container {
            max-width: 900px;
            padding-top: 3rem;
            padding-bottom: 2rem;
        }

        </style>
    """, unsafe_allow_html=True)


    # Initialize auth mode
    if "manager_auth_mode" not in st.session_state:
        st.session_state["manager_auth_mode"] = "login"
    header_col, back_col = st.columns(
        [3, 1],
        vertical_alignment="center"
    )

    with header_col:
        render_header()
    with back_col:
        if st.button("← Back",type="secondary",key="manager_back_button",use_container_width=True):
            st.session_state["login_type"] = None
            st.session_state["manager_auth_mode"] = "login"
            st.rerun()

    # LOGIN SCREEN 

    if st.session_state["manager_auth_mode"] == "login":
        st.header("Manager Login")
        st.write("Sign in to manage your inventory workspace.")
        st.space()

        manager_email = st.text_input("Email",placeholder="Enter your email", key="manager_login_email")

        manager_password = st.text_input( "Password",type="password",key="manager_login_password",placeholder="enter password")

        st.divider()

        if st.button(
            "Login as Manager",
            type="primary",
            key="manager_login_button",
            use_container_width=True
        ):

            if not manager_email or not manager_password:
                st.error("Please enter your email and password.")

            else:
                manager = manager_login(
                    manager_email,
                    manager_password
                )

                if manager:
                    st.session_state["is_authenticated"] = True
                    st.session_state["user"] = manager
                    st.session_state["login_type"] = "manager_dashboard"
                    st.rerun()

                else:
                    st.error("Invalid email or password.")


        st.space("small")

        register_col1, register_col2 = st.columns(  [1.4, 0.8],gap="small")

        with register_col1:
            st.write("Don't have a manager account?")

        with register_col2:
            if st.button("Create Account",type="secondary",key="manager_register_switch",use_container_width=True):
                st.session_state["manager_auth_mode"] = "register"
                st.rerun()


    #  REGISTER SCREEN

    else:

        st.header("Create Manager Account")

        st.write("Create an account to manage your inventory workspace.")

        st.space()

        manager_name = st.text_input("Full Name",placeholder="Enter your full name", key="manager_register_name")

        manager_email = st.text_input( "Email",placeholder="Enter your email", key="manager_register_email")

        manager_password = st.text_input("Password",type="password", placeholder="Create a password", key="manager_register_password")

        confirm_password = st.text_input( "Confirm Password",type="password",placeholder="Confirm your password",key="manager_confirm_password")

        st.divider()

        if st.button( "Create Manager Account",type="primary", key="manager_register_button",use_container_width=True ):

            if (not manager_name or not manager_email or not manager_password or not confirm_password):
                st.error("Please fill in all fields.")

            elif manager_password != confirm_password:
                st.error("Passwords do not match.")

            elif check_email_exists(manager_email):
                st.error("An account with this email already exists.")

            else:
                try:
                    create_manager(manager_name, manager_email,manager_password )

                    st.success("Account created successfully!")

                    # Switch back to login page
                    st.session_state["manager_auth_mode"] = "login"

                except Exception as error:
                    st.error(f"Unable to create account: {error}")


        st.space("small")

        login_col1, login_col2 = st.columns([1.4, 0.8],gap="small" )
        
        with login_col1:
            st.write("Already have an account?")

        with login_col2:
            if st.button(
                "Sign in",type="secondary",key="manager_register_switch",use_container_width=True
            ):
                st.session_state["manager_auth_mode"] = "login"
                st.rerun()


    # Footer
    st.space("large")
    render_footer()