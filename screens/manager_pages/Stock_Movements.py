import streamlit as st

from utils.layout import style_base_layout
from manager_services.item_service import get_items
from manager_services.location_service import get_locations
from manager_services.stock_movement_service import create_stock_movement
from manager_services.stock_movement_service import get_recent_stock_movements
from datetime import datetime
def stock_movement_page():

    style_base_layout()

    # ---------- DASHBOARD QUICK ACTION ----------

    if st.session_state.get("dashboard_action") == "receive_stock":

        st.session_state.show_receive_stock_form = True
        st.session_state.show_transfer_stock_form = False

        st.session_state.pop("dashboard_action")


    elif st.session_state.get("dashboard_action") == "transfer_stock":

        st.session_state.show_transfer_stock_form = True
        st.session_state.show_receive_stock_form = False

        st.session_state.pop("dashboard_action")

    items = get_items()
    locations = get_locations()

    item_options = {
        item["name"]: item["id"]
        for item in items
    }

    active_locations = [
        location
        for location in locations
        if location["is_active"]
    ]

    location_options = {
        location["name"]: location["id"]
        for location in active_locations
    }

    # ---------- SESSION STATE ----------

    if "show_stock_movement_form" not in st.session_state:
        st.session_state.show_stock_movement_form = False

    # ---------- HEADER ----------

    title_col, button_col = st.columns([4, 1])

    with title_col:
        st.title("Stock Movements")
        st.caption("Record and track inventory stock movements.")

    with button_col:
        st.write("")
        st.write("")

        if st.button(
            "＋ Record Movement",
            use_container_width=True
        ):
            st.session_state.show_stock_movement_form = True

    st.write("")

     # ---------- MOVEMENT FORM ----------

    if st.session_state.show_stock_movement_form:

        st.subheader("Record Stock Movement")

        # ---------- MOVEMENT TYPE ----------

        movement_type = st.selectbox(
            "Movement Type",
            ["receipt", "issue", "adjustment", "transfer"],
            format_func=lambda x: x.capitalize()
        )

        st.write("")

        # ---------- ITEM ----------

        item_col, quantity_col = st.columns([2, 1])

        with item_col:
            item_name = st.selectbox(
                "Item",
                ["Select Item"] + list(item_options.keys())
            )

        with quantity_col:
            quantity = st.number_input(
                "Quantity",
                min_value=1.0,
                value=1.0,
                step=1.0
            )

        # ==================================================
        # RECEIPT / ISSUE / ADJUSTMENT
        # ==================================================

        if movement_type in ["receipt", "issue", "adjustment"]:

            location_name = st.selectbox(
            "Location",
            ["Select Location"] + list(location_options.keys())
        )

        # ==================================================
        # TRANSFER
        # ==================================================

        elif movement_type == "transfer":
            source_col, gap, destination_col = st.columns([2, 0.08, 2])

            with source_col:
                source_location_name = st.selectbox(
                    "Source Location",
                    ["Select Source Location"] + list(location_options.keys())
                )

            with destination_col:
                destination_location_name = st.selectbox(
                    "Destination Location",
                    ["Select Destination Location"] + list(location_options.keys())
                )

        # ==================================================
        # ADJUSTMENT DETAILS
        # ==================================================

        if movement_type == "adjustment":

            direction_col, gap, reason_col = st.columns([1, 0.08, 2])

            with direction_col:
                adjustment_direction = st.selectbox(
                    "Adjustment Direction",
                    ["increase", "decrease"],
                    format_func=lambda x: x.capitalize()
                )

            with reason_col:
                adjustment_reason = st.text_input(
                    "Adjustment Reason",
                    placeholder="Why is the stock being adjusted?"
                )

        st.write("")

        # ---------- BUTTONS ----------

        cancel_col, save_col, _ = st.columns([1, 1, 2])

        with cancel_col:
            if st.button(
                "Cancel",
                use_container_width=True,
                key="cancel_stock_movement"
            ):
                st.session_state.show_stock_movement_form = False
                st.rerun()

        with save_col:
            if st.button(
                "Save Movement",
                use_container_width=True,
                type="primary",
                key="save_stock_movement"
            ):

                # ---------- ITEM VALIDATION ----------

                if item_name == "Select Item":
                    st.error("Please select an item.")

                # ---------- RECEIPT / ISSUE / ADJUSTMENT ----------

                elif movement_type in ["receipt", "issue", "adjustment"]:

                    if location_name == "Select Location":
                        st.error("Please select a location.")

                    elif movement_type == "adjustment" and not adjustment_reason.strip():
                        st.error("Please enter an adjustment reason.")

                    else:
                        try:
                            create_stock_movement(
                                item_id=item_options[item_name],
                                movement_type=movement_type,
                                quantity=quantity,
                                recorded_by=st.session_state["user"]["id"],
                                location_id=location_options[location_name],
                                adjustment_reason=(
                                    adjustment_reason.strip()
                                    if movement_type == "adjustment"
                                    else None
                                ),
                                adjustment_direction=(
                                    adjustment_direction
                                    if movement_type == "adjustment"
                                    else None
                                )
                            )

                            st.success("Stock movement recorded successfully!")

                            st.session_state.show_stock_movement_form = False
                            st.rerun()

                        except Exception as e:

                            error_message = str(e)

                            if "Insufficient stock" in error_message:
                                    st.info("Insufficient stock to issue.")

                            else:
                                    st.error("Unable to record the stock movement. Please try again.")

                # ---------- TRANSFER ----------

                elif movement_type == "transfer":

                    if source_location_name == "Select Source Location":
                        st.error("Please select a source location.")

                    elif destination_location_name == "Select Destination Location":
                        st.error("Please select a destination location.")

                    elif source_location_name == destination_location_name:
                        st.error(
                            "Source and destination locations cannot be the same."
                        )

                    else:
                        try:
                            create_stock_movement(
                                item_id=item_options[item_name],
                                movement_type="transfer",
                                quantity=quantity,
                                recorded_by=st.session_state["user"]["id"],
                                source_location_id=(
                                    location_options[source_location_name]
                                ),
                                destination_location_id=(
                                    location_options[destination_location_name]
                                )
                            )

                            st.success("Stock transfer recorded successfully!")

                            st.session_state.show_stock_movement_form = False
                            st.rerun()

                        except Exception as error:

                            error_message = str(error)

                            if "Insufficient stock" in error_message:

                                import re

                                match = re.search(
                                    r"Available:\s*([0-9.]+),\s*Requested:\s*([0-9.]+)",
                                    error_message
                                )

                                if match:

                                    available = match.group(1)
                                    requested = match.group(2)

                                    st.warning(
                                        f"Only {available} units are currently available "
                                        f"at the source location. "
                                        f"Please enter a quantity of {available} or less."
                                    )

                                else:

                                    st.warning(
                                        "The requested quantity is greater than the available stock."
                                    )

                            else:
                                st.error(
                                    "Unable to record the stock movement. Please try again."
                                )

                st.divider()

    # ---------- RECENT MOVEMENTS ----------

    st.subheader("Recent Movements")

    recent_movements = get_recent_stock_movements()

    if not recent_movements:
        st.info("No stock movements recorded yet.")

    else:

        # ---------- TABLE HEADER ----------

        col1, col2, col3, col4, col5 = st.columns(
            [1.2, 1.5, 0.7, 1.3, 1.2]
        )

        with col1:
            st.caption("Item")

        with col2:
            st.caption("Type")

        with col3:
            st.caption("Quantity")

        with col4:
            st.caption("Location / Route")

        with col5:
            st.caption("Time")

        st.divider()


        # ---------- MOVEMENT ROWS ----------

        for movement in recent_movements:

            item = movement.get("items") or {}
            location = movement.get("locations") or {}

            source_location = (
                movement.get("source_location") or {}
            )

            destination_location = (
                movement.get("destination_location") or {}
            )

            movement_type = movement["movement_type"]
            quantity = movement["quantity"]


            # ---------- LOCATION / ROUTE ----------

            if movement_type == "transfer":

                movement_location = (
                    f"{source_location.get('name', '-')} → "
                    f"{destination_location.get('name', '-')}"
                )

            else:

                movement_location = location.get("name", "-")


            # ---------- TYPE ----------

            type_display = {
                "receipt": "📥 Receipt",
                "issue": "📤 Issue",
                "transfer": "🚚 Transfer",
                "adjustment": "⚙️ Adjustment"
            }.get(
                movement_type,
                movement_type.capitalize()
            )


            # ---------- QUANTITY ----------

            if movement_type == "receipt":

                quantity_display = f"+{quantity}"

            elif movement_type == "issue":

                quantity_display = f"-{quantity}"

            elif (
                movement_type == "adjustment"
                and movement.get("adjustment_direction") == "increase"
            ):

                quantity_display = f"+{quantity}"

            elif (
                movement_type == "adjustment"
                and movement.get("adjustment_direction") == "decrease"
            ):

                quantity_display = f"-{quantity}"

            else:

                quantity_display = str(quantity)


            # ---------- TIME ----------

            formatted_time = datetime.fromisoformat(
                movement["created_at"].replace("Z", "+00:00")
            ).strftime("%d %b %Y, %H:%M")


            # ---------- DISPLAY ROW ----------

            col1, col2, col3, col4, col5 = st.columns(
                [1.2, 1.5, 0.7, 1.3, 1.2]
            )

            with col1:
                st.write(item.get("name", "-"))

            with col2:
                st.write(type_display)

            with col3:
                st.write(quantity_display)

            with col4:
                st.write(movement_location)

            with col5:
                st.write(formatted_time)

        st.divider()