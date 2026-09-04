import streamlit as st
from utils.layout import (style_base_layout, style_background_home)

from utils.header import render_header
from utils.footer import render_footer
from utils.auth import (check_email_exists, create_staff,staff_login)
from screens.staff import staff_screen

def staff_auth_screen():

    # ---------- OPEN STAFF SCREEN AFTER LOGIN ----------

    if (
        st.session_state.get("is_authenticated")
        and st.session_state.get("login_type") == "staff"
    ):
        staff_screen()
        return


    style_base_layout()
    style_background_home()


    if "staff_auth_mode" not in st.session_state:
        st.session_state["staff_auth_mode"] = "login"


    auth_mode = st.session_state["staff_auth_mode"]


    # ---------- CENTERED PAGE LAYOUT ----------

    left_space, content_col, right_space = st.columns(
        [1, 1.6, 1]
    )


    with content_col:

        # ---------- HEADER ----------

        header_col, back_col = st.columns(
            [3, 1],
            vertical_alignment="center"
        )

        with header_col:
            render_header()

        with back_col:

            if st.button(
                "← Back",
                key="staff_back_button",
                type="secondary",
                use_container_width=True
            ):

                st.session_state["login_type"] = None
                st.session_state["staff_auth_mode"] = "login"

                st.rerun()


        # ==================================================
        # LOGIN SCREEN
        # ==================================================

        if auth_mode == "login":

            st.header("Staff Login")

            st.write(
                "Sign in to manage stock at your assigned locations."
            )

            st.space()


            staff_email = st.text_input(
                "Email",
                placeholder="Enter your email",
                key="staff_login_email"
            )


            staff_password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="staff_login_password"
            )


            st.divider()


            if st.button(
                "Login as Staff",
                type="primary",
                key="staff_login_button",
                use_container_width=True
            ):

                if not staff_email or not staff_password:

                    st.error(
                        "Please enter your email and password."
                    )

                else:

                    staff = staff_login(
                        staff_email,
                        staff_password
                    )

                    if staff:

                        st.session_state["current_user"] = staff
                        st.session_state["user"] = staff
                        st.session_state["is_authenticated"] = True
                        st.session_state["login_type"] = "staff"

                        st.rerun()

                    else:

                        st.error(
                            "Invalid email or password."
                        )


            st.space("small")


            register_col1, register_col2 = st.columns(
                [1.4, 0.8],
                gap="small"
            )


            with register_col1:

                st.write(
                    "Don't have a staff account?"
                )


            with register_col2:

                if st.button(
                    "Create Account",
                    type="secondary",
                    key="staff_register_switch",
                    use_container_width=True
                ):

                    st.session_state[
                        "staff_auth_mode"
                    ] = "register"

                    st.rerun()


        # ==================================================
        # REGISTER SCREEN
        # ==================================================

        else:

            st.header("Create Staff Account")

            st.write(
                "Create an account to manage inventory at "
                "your assigned locations."
            )

            st.space()


            staff_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name",
                key="staff_register_name"
            )


            staff_email = st.text_input(
                "Email",
                placeholder="Enter your email",
                key="staff_register_email"
            )


            staff_password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password",
                key="staff_register_password"
            )


            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm your password",
                key="staff_confirm_password"
            )


            st.divider()


            if st.button(
                "Create Staff Account",
                type="primary",
                key="staff_register_button",
                use_container_width=True
            ):

                if (
                    not staff_name
                    or not staff_email
                    or not staff_password
                    or not confirm_password
                ):

                    st.error(
                        "Please fill in all fields."
                    )


                elif staff_password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )


                elif check_email_exists(staff_email):

                    st.error(
                        "An account with this email already exists."
                    )


                else:

                    try:

                        create_staff(
                            staff_name,
                            staff_email,
                            staff_password
                        )

                        st.success(
                            "Staff account created successfully! "
                            "Please sign in."
                        )

                        st.session_state[
                            "staff_auth_mode"
                        ] = "login"

                    except Exception as error:

                        st.error(
                            f"Unable to create account: {error}"
                        )


            st.space("small")


            login_col1, login_col2 = st.columns(
                [1.4, 0.8],
                gap="small"
            )


            with login_col1:

                st.write(
                    "Already have an account?"
                )


            with login_col2:

                if st.button(
                    "Sign in",
                    type="secondary",
                    key="staff_login_switch",
                    use_container_width=True
                ):

                    st.session_state[
                        "staff_auth_mode"
                    ] = "login"

                    st.rerun()


        # ---------- FOOTER ----------

        render_footer()