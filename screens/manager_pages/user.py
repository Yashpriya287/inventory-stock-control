import streamlit as st

from utils.layout import style_base_layout
from manager_services.user_service import ( get_staff_users,update_staff_status, get_staff_locations, update_staff_locations)
from manager_services.location_service import get_locations


def users_page():

    style_base_layout()
    if "show_add_staff_form" not in st.session_state:
        st.session_state.show_add_staff_form = False

    if st.session_state.get("dashboard_action") == "add_staff":
        st.session_state.show_add_staff_form = True
        st.session_state.pop("dashboard_action")

    st.markdown("""
    <style>

    /* ---------- DIALOG ---------- */

    div[data-testid="stDialog"] > div {
        background-color: #1B2436 !important;
        color: #FFFFFF !important;
    }

    div[data-testid="stDialog"] {
        color: #FFFFFF !important;
    }

    /* Text inside dialog */

    div[data-testid="stDialog"] p,
    div[data-testid="stDialog"] span,
    div[data-testid="stDialog"] label {
        color: #FFFFFF !important;
    }

    /* Dialog close button */

    div[data-testid="stDialog"] button {
        color: #FFFFFF !important;
    }

    /* ---------- MULTISELECT BOX ---------- */

    div[data-testid="stDialog"] [data-baseweb="select"] > div {
        background-color: #2D3A52 !important;
        border: 1px solid #556785 !important;
        color: #FFFFFF !important;
    }

    /* Input and selected text */

    div[data-testid="stDialog"] [data-baseweb="select"] input {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* Placeholder */

    div[data-testid="stDialog"] [data-baseweb="select"] input::placeholder {
        color: #AEB9CC !important;
        opacity: 1 !important;
    }

    /* Dropdown arrow */

    div[data-testid="stDialog"] [data-baseweb="select"] svg {
        fill: #FFFFFF !important;
    }

    /* ---------- DROPDOWN MENU ---------- */

    div[role="listbox"] {
        background-color: #2D3A52 !important;
    }

    div[role="option"] {
        background-color: #2D3A52 !important;
        color: #FFFFFF !important;
    }

    div[role="option"]:hover {
        background-color: #3A4A66 !important;
    }

    </style>
    """, unsafe_allow_html=True)

    st.title("Users")
    st.caption("Manage staff accounts and assign locations they can access.")
    st.write("")
    #  GET DATA 
    staff_users = get_staff_users()
    locations = get_locations()
    active_locations = [
        location
        for location in locations
        if location["is_active"]
    ]
    # Location name -> location ID
    location_options = {
        location["name"]: location["id"]
        for location in active_locations
    }
    # Location ID -> location name
    location_id_to_name = {
        location["id"]: location["name"]
        for location in active_locations
    }
    # All location names

    location_names = list(location_options.keys())

    # ---------- LOCATION DIALOG ----------

    @st.dialog(" ")
    def manage_locations_dialog(user):

        # ---------- DIALOG TITLE ----------

        st.markdown(
            """
            <div style="
                font-size: 22px;
                font-weight: 700;
                color: white;
                margin-bottom: 10px;
            ">
                Assign Locations
            </div>
            """,
            unsafe_allow_html=True
        )


        # ---------- DESCRIPTION ----------

        st.write(
            f"Select the locations that **{user['full_name']}** can access."
        )


        # ---------- CURRENT ASSIGNMENTS ----------

        assigned_location_ids = get_staff_locations(
            user["id"]
        )


        # Convert assigned IDs to location names

        assigned_location_names = [
            location_id_to_name[location_id]
            for location_id in assigned_location_ids
            if location_id in location_id_to_name
        ]


        # ---------- LOCATION MULTISELECT ----------

        selected_locations = st.multiselect(
            "Locations",
            options=location_names,
            default=assigned_location_names,
            placeholder="Select locations",
            key=f"assign_locations_multiselect_{user['id']}"
        )


        # ---------- ACTION BUTTONS ----------

        save_col, cancel_col = st.columns(2)


        # ---------- SAVE ----------

        with save_col:

            if st.button(
                "Save",
                type="primary",
                key=f"save_locations_{user['id']}",
                use_container_width=True
            ):

                # Convert selected names to IDs

                selected_location_ids = [
                    location_options[location_name]
                    for location_name in selected_locations
                ]


                # Update all assignments

                update_staff_locations(
                    user["id"],
                    selected_location_ids
                )


                # Close dialog and refresh page

                st.rerun()


        # ---------- CANCEL ----------

        with cancel_col:

            if st.button(
                "Cancel",
                key=f"cancel_locations_{user['id']}",
                use_container_width=True
            ):

                st.rerun()

    # ---------- NO USERS ----------

    if not staff_users:

        st.info("No staff accounts have been created yet.")

    else:

        # ---------- TABLE HEADER ----------

        (
            name_col,
            email_col,
            role_col,
            status_col,
            location_col,
            action_col
        ) = st.columns([1.5, 2, 1, 1.2, 1.8, 1.5])

        with name_col:
            st.caption("Name")

        with email_col:
            st.caption("Email")

        with role_col:
            st.caption("Role")

        with status_col:
            st.caption("Status")

        with location_col:
            st.caption("Assigned Locations")

        with action_col:
            st.caption("Action")

        st.divider()

        # ---------- USER ROWS ----------

        for user in staff_users:

            (
                name_col,
                email_col,
                role_col,
                status_col,
                location_col,
                action_col
            ) = st.columns([1.5, 2, 1, 1.2, 1.8, 1.5])

            with name_col:

                st.markdown(
                    f"**{user['full_name']}**"
                )

            with email_col:

                st.write(
                    user["email"]
                )

            with role_col:

                st.write(
                    user["role"].capitalize()
                )

            with status_col:

                if user["is_active"]:

                    st.write("🟢 Active")

                else:

                    st.write("🔴 Inactive")

            with location_col:

                assigned_location_ids = get_staff_locations(user["id"])

                assigned_location_names = [
                    location["name"]
                    for location in active_locations
                    if location["id"] in assigned_location_ids
                ]

                if assigned_location_names:

                    st.write(
                        ", ".join(assigned_location_names)
                    )

                else:

                    st.write("No locations assigned")

            with action_col:

                action1, action2 = st.columns(2)

                # ---------- ACTIVATE / DEACTIVATE ----------

                with action1:

                    if user["is_active"]:

                        if st.button(
                            "Deactivate",
                            key=f"deactivate_{user['id']}",
                            use_container_width=True
                        ):

                            try:

                                update_staff_status(
                                    user["id"],
                                    False
                                )

                                st.success(
                                    f"{user['full_name']} deactivated."
                                )

                                st.rerun()

                            except Exception as error:

                                st.error(
                                    f"Unable to deactivate user: {error}"
                                )

                    else:

                        if st.button(
                            "Activate",
                            key=f"activate_{user['id']}",
                            type="primary",
                            use_container_width=True
                        ):

                            try:

                                update_staff_status(
                                    user["id"],
                                    True
                                )

                                st.success(
                                    f"{user['full_name']} activated."
                                )

                                st.rerun()

                            except Exception as error:

                                st.error(
                                    f"Unable to activate user: {error}"
                                )

                # ---------- MANAGE LOCATIONS ----------

                with action2:

                    if st.button(
                        "Manage",
                        key=f"locations_{user['id']}",
                        use_container_width=True
                    ):

                        manage_locations_dialog(user)

            st.divider()