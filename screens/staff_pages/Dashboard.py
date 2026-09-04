import streamlit as st

from utils.layout import style_base_layout

from staff_services.staff_dashboard_service import (
    get_staff_locations,
    get_staff_low_stock_items,
    get_staff_recent_activity
)


def staff_dashboard_page():

    style_base_layout()
    def open_movement_page(movement_type):

        st.session_state["staff_selected_page"] = (
            "↔️  Stock Movements"
        )

        st.session_state["staff_movement_type"] = (
            movement_type
        )

    # ==================================================
    # CURRENT USER
    # ==================================================

    current_user = st.session_state.get(
        "current_user"
    )

    if not current_user:

        st.warning(
            "Please log in first."
        )

        return

    staff_id = current_user["id"]

    # ==================================================
    # GET DASHBOARD DATA
    # ==================================================

    assigned_locations = get_staff_locations(
        staff_id
    )


    low_stock_items = get_staff_low_stock_items(
        staff_id
    )

    recent_activity = get_staff_recent_activity(
        staff_id,
        limit=3
    )

    # ==================================================
    # HEADER
    # ==================================================

    st.title("Staff Dashboard")

    st.caption(
        f"Welcome back, {current_user['full_name']} 👋"
    )

    st.write(
        "Manage stock movements across your assigned locations."
    )


    # ==================================================
    # ASSIGNED LOCATIONS
    # ==================================================

    st.subheader("Assigned Locations")

    if assigned_locations:

        location_names = [

            location["name"]

            for location in assigned_locations

        ]
        st.write( " • ".join(location_names))
    else:
        st.info("You have not been assigned to any locations yet.")

    st.divider()

    # ==================================================
    # QUICK ACTIONS
    # ==================================================

    st.subheader("Quick Actions")

    action_col1, action_col2, action_col3 = (
        st.columns(3)
    )

    # ---------- RECORD RECEIPT ----------

    with action_col1:

        st.button(
            "📥 Record Receipt",
            use_container_width=True,
            on_click=open_movement_page,
            args=("Receipt",)
        )

    # ---------- RECORD ISSUE ----------

    with action_col2:

        st.button(
            "📤 Record Issue",
            use_container_width=True,
            on_click=open_movement_page,
            args=("Issue",)
        )

    # ---------- TRANSFER STOCK ----------

    with action_col3:

        st.button(
            "🔄 Transfer Stock",
            use_container_width=True,
            on_click=open_movement_page,
            args=("Transfer",)
        )
    st.divider()

    # ==================================================
    # RECENT ACTIVITY AND LOW STOCK ALERTS
    # ==================================================

    activity_col, alert_col = st.columns(2)

    # ---------- RECENT ACTIVITY ----------

    with activity_col:

        st.subheader(
            "Recent Activity"
        )

        if not recent_activity:

            st.info(
                "No recent activity."
            )

        else:

            for movement in recent_activity:

                movement_type = (
                    movement["movement_type"]
                    .capitalize()
                )

                item = (
                    movement.get("items")
                    or {}
                )

                item_name = item.get(
                    "name",
                    "Unknown Item"
                )

                quantity = float(
                    movement["quantity"]
                )

                # ---------- LOCATION ----------

                if movement["movement_type"] == "Transfer":

                    source_location = (
                        movement.get("source_location")
                        or {}
                    )

                    destination_location = (
                        movement.get(
                            "destination_location"
                        )
                        or {}
                    )

                    source_name = source_location.get(
                        "name",
                        "-"
                    )

                    destination_name = (
                        destination_location.get(
                            "name",
                            "-"
                        )
                    )

                    location_text = (
                        f"{source_name} → "
                        f"{destination_name}"
                    )

                else:

                    location = (
                        movement.get("locations")
                        or {}
                    )

                    location_text = location.get(
                        "name",
                        "-"
                    )

                # ---------- ACTIVITY ROW ----------

                st.info(
                    f"**{movement_type}: "
                    f"{quantity:.1f} {item_name}** "
                    f"→ {location_text}"
                )

   # ---------- LOW STOCK ALERTS ----------

    with alert_col:

        st.subheader(
            "Low Stock Alerts"
        )

        if not low_stock_items:

            st.success(
                "All assigned inventory is above "
                "the reorder level."
            )

        else:

            for item in low_stock_items[:5]:

                st.warning(
                    f"⚠️ {item['name']} → "
                    f"{item['location_name']}"
                )