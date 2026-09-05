import streamlit as st

from utils.layout import style_base_layout

from staff_services.staff_movement_services import (
    get_staff_locations,
    get_active_items,
    get_items_with_stock,
    create_staff_stock_movement,
    get_staff_recent_movements
)
from datetime import datetime
from zoneinfo import ZoneInfo

def staff_stock_movements_page():

    style_base_layout()

    # ---------- CURRENT USER ----------

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in first.")
        return

    staff_id = current_user["id"]

    # ---------- SESSION STATE ----------

    if "staff_movement_form" not in st.session_state:
        st.session_state["staff_movement_form"] = None

    # ---------- GET DATABASE DATA ----------

    assigned_locations = get_staff_locations(staff_id)

    active_items = get_active_items()

    # ---------- HEADER ----------

    st.title("Stock Movements")

    st.caption(
        "Record stock movements for your assigned locations."
    )

    st.write("")

    # ---------- MOVEMENT ACTIONS ----------

    receipt_col, issue_col, transfer_col = st.columns(3)

    with receipt_col:

        if st.button(
            "📥 Receive Stock",
            use_container_width=True
        ):

            st.session_state[
                "staff_movement_form"
            ] = "receipt"

            st.rerun()

    with issue_col:

        if st.button(
            "📤 Issue Stock",
            use_container_width=True
        ):

            st.session_state[
                "staff_movement_form"
            ] = "issue"

            st.rerun()

    with transfer_col:

        if st.button(
            "↔️ Transfer Stock",
            use_container_width=True
        ):

            st.session_state[
                "staff_movement_form"
            ] = "transfer"

            st.rerun()

    # ==================================================
    # RECEIVE STOCK
    # ==================================================

    if st.session_state["staff_movement_form"] == "receipt":

        st.divider()

        st.subheader("Receive Stock")

        if not assigned_locations:

            st.warning(
                "You have not been assigned to any locations."
            )

            return

        # ---------- ITEM OPTIONS ----------

        item_options = {
            f"{item['name']} ({item['sku']})": item
            for item in active_items
        }

        # ---------- LOCATION OPTIONS ----------

        location_options = {
            location["name"]: location["id"]
            for location in assigned_locations
        }

        item_col, location_col = st.columns(2)

        with item_col:

            selected_item_name = st.selectbox(
                "Item",
                list(item_options.keys()),
                key="staff_receipt_item"
            )

        with location_col:

            selected_location_name = st.selectbox(
                "Location",
                list(location_options.keys()),
                key="staff_receipt_location"
            )

        # ---------- QUANTITY ----------

        quantity = st.number_input(
            "Quantity",
            min_value=0.0,
            step=1.0,
            key="staff_receipt_quantity"
        )

        # ---------- SELECTED VALUES ----------

        selected_item = item_options[
            selected_item_name
        ]

        selected_location_id = location_options[
            selected_location_name
        ]

        # ---------- BUTTONS ----------

        cancel_col, save_col, empty_col = st.columns(
            [1, 1, 3]
        )

        with cancel_col:

            if st.button(
                "Cancel",
                use_container_width=True,
                key="cancel_staff_receipt"
            ):

                st.session_state[
                    "staff_movement_form"
                ] = None

                st.rerun()

        with save_col:

            if st.button(
                "Record Receipt",
                type="primary",
                use_container_width=True,
                key="save_staff_receipt"
            ):

                if quantity <= 0:

                    st.error(
                        "Quantity must be greater than zero."
                    )

                else:

                    try:

                        create_staff_stock_movement(
                            user_id=staff_id,
                            item_id=selected_item["id"],
                            movement_type="receipt",
                            quantity=quantity,
                            location_id=selected_location_id
                        )

                        st.success(
                            "Stock receipt recorded successfully!"
                        )

                        st.session_state[
                            "staff_movement_form"
                        ] = None

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Error recording receipt: {e}"
                        )

    # ==================================================
    # ISSUE STOCK
    # ==================================================

    elif st.session_state["staff_movement_form"] == "issue":

        st.divider()

        st.subheader("Issue Stock")

        if not assigned_locations:

            st.warning(
                "You have not been assigned to any locations."
            )

            return

        # ---------- LOCATION OPTIONS ----------

        location_options = {
            location["name"]: location["id"]
            for location in assigned_locations
        }

        location_col, empty_col = st.columns(2)

        with location_col:

            selected_location_name = st.selectbox(
                "Location",
                list(location_options.keys()),
                key="staff_issue_location"
            )

        selected_location_id = location_options[
            selected_location_name
        ]

        # ---------- GET ITEMS AVAILABLE AT LOCATION ----------

        available_items = get_items_with_stock(
            selected_location_id
        )

        if not available_items:

            st.info(
                "No items with available stock at this location."
            )

        else:

            item_options = {
                f"{item['name']} ({item['sku']})": item
                for item in available_items
            }

            # ---------- ITEM AND QUANTITY ----------

            item_col, quantity_col, empty_col = st.columns([2, 1, 1])

            with item_col:

                selected_item_name = st.selectbox(
                    "Item",
                    list(item_options.keys()),
                    key="staff_issue_item"
                )

                selected_item = item_options[
                    selected_item_name
                ]

                st.caption(
                    f"Available stock: "
                    f"**{selected_item['available_stock']}**"
                )

            with quantity_col:

                quantity = st.number_input(
                    "Quantity",
                    min_value=0.0,
                    step=1.0,
                    key="staff_issue_quantity"
                )
            cancel_col, save_col, empty_col = st.columns(
                    [1, 1, 3]
            )

            with cancel_col:

                if st.button(
                    "Cancel",
                    use_container_width=True,
                    key="cancel_staff_issue"
                ):

                    st.session_state[
                        "staff_movement_form"
                    ] = None

                    st.rerun()

            with save_col:

                if st.button(
                    "Record Issue",
                    type="primary",
                    use_container_width=True,
                    key="save_staff_issue"
                ):

                    if quantity <= 0:

                        st.error(
                            "Quantity must be greater than zero."
                        )

                    elif quantity > selected_item[
                        "available_stock"
                    ]:

                        st.error(
                            "Insufficient stock at this location."
                        )

                    else:

                        try:

                            create_staff_stock_movement(
                                user_id=staff_id,
                                item_id=selected_item["id"],
                                movement_type="issue",
                                quantity=quantity,
                                location_id=selected_location_id
                            )

                            st.success(
                                "Stock issue recorded successfully!"
                            )

                            st.session_state[
                                "staff_movement_form"
                            ] = None

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Error recording issue: {e}"
                            )

    # ==================================================
    # TRANSFER STOCK
    # ==================================================

    elif st.session_state["staff_movement_form"] == "transfer":

        st.divider()

        st.subheader("Transfer Stock")

        if len(assigned_locations) < 2:

            st.warning(
                "You must be assigned to at least two locations "
                "to transfer stock."
            )

            return

        location_options = {
            location["name"]: location["id"]
            for location in assigned_locations
        }

        source_col, destination_col = st.columns(2)

        with source_col:

            selected_source_name = st.selectbox(
                "From Location",
                list(location_options.keys()),
                key="staff_transfer_source"
            )

        source_location_id = location_options[
            selected_source_name
        ]

        # ---------- ITEMS AT SOURCE LOCATION ----------

        available_items = get_items_with_stock(
            source_location_id
        )

        # ---------- DESTINATION LOCATIONS ----------

        destination_names = [
            location["name"]
            for location in assigned_locations
            if location["id"] != source_location_id
        ]

        with destination_col:

            selected_destination_name = st.selectbox(
                "To Location",
                destination_names,
                key="staff_transfer_destination"
            )

        destination_location_id = location_options[
            selected_destination_name
        ]

        if not available_items:

            st.info(
                "No items with available stock "
                "at the source location."
            )

        else:

            item_options = {
                f"{item['name']} ({item['sku']})": item
                for item in available_items
            }

            # ---------- ITEM AND QUANTITY ----------

            item_col, quantity_col, empty_col = st.columns([2, 1, 1])

            with item_col:

                selected_item_name = st.selectbox(
                    "Item",
                    list(item_options.keys()),
                    key="staff_issue_item"
                )

                selected_item = item_options[
                    selected_item_name
                ]

                st.caption(
                    f"Available stock: "
                    f"**{selected_item['available_stock']}**"
                )

            with quantity_col:

                quantity = st.number_input(
                    "Quantity",
                    min_value=0.0,
                    step=1.0,
                    key="staff_issue_quantity"
                )

            cancel_col, save_col, empty_col = st.columns(
                [1, 1, 3]
            )

            with cancel_col:

                if st.button(
                    "Cancel",
                    use_container_width=True,
                    key="cancel_staff_transfer"
                ):

                    st.session_state[
                        "staff_movement_form"
                    ] = None

                    st.rerun()

            with save_col:

                if st.button(
                    "Record Transfer",
                    type="primary",
                    use_container_width=True,
                    key="save_staff_transfer"
                ):

                    if quantity <= 0:

                        st.error(
                            "Quantity must be greater than zero."
                        )

                    elif quantity > selected_item[
                        "available_stock"
                    ]:

                        st.error(
                            "Insufficient stock at the source location."
                        )

                    else:

                        try:

                            create_staff_stock_movement(
                                user_id=staff_id,
                                item_id=selected_item["id"],
                                movement_type="transfer",
                                quantity=quantity,
                                source_location_id=source_location_id,
                                destination_location_id=destination_location_id
                            )

                            st.success(
                                "Stock transfer recorded successfully!"
                            )

                            st.session_state[
                                "staff_movement_form"
                            ] = None

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Error recording transfer: {e}"
                            )

    # ==================================================
    # RECENT MOVEMENTS
    # ==================================================

    st.divider()

    st.subheader("Recent Movements")

    recent_movements = get_staff_recent_movements(
        staff_id
    )

    if not recent_movements:

        st.info(
            "No recent movements found at your assigned locations."
        )

    else:

        for movement in recent_movements:

            item = movement.get("items") or {}

            item_name = item.get(
                "name",
                "Unknown Item"
            )

            movement_type = (
                movement.get("movement_type") or ""
            ).lower()

            quantity = movement.get("quantity", 0)

            # ---------- TRANSFER ----------

            if movement_type == "transfer":

                source = (
                    movement.get("source_location") or {}
                ).get(
                    "name",
                    "Unknown"
                )

                destination = (
                    movement.get("destination_location") or {}
                ).get(
                    "name",
                    "Unknown"
                )

                st.info(
                    f"↔️ **Transfer:** {quantity} "
                    f"{item_name} — "
                    f"**{source} → {destination}**"
                )

            # ---------- RECEIPT ----------

            elif movement_type == "receipt":

                location = (
                    movement.get("locations") or {}
                ).get(
                    "name",
                    "Unknown Location"
                )

                st.success(
                    f"📥 **Receipt:** {quantity} "
                    f"{item_name} → "
                    f"**{location}**"
                )

            # ---------- ISSUE ----------

            elif movement_type == "issue":

                location = (
                    movement.get("locations") or {}
                ).get(
                    "name",
                    "Unknown Location"
                )

                st.warning(
                    f"📤 **Issue:** {quantity} "
                    f"{item_name} → "
                    f"**{location}**"
                )

            # ---------- RECORDED BY ----------

            user = movement.get("users") or {}

            recorded_by = user.get(
                "full_name",
                "Unknown User"
            )


            # ---------- RECORDED AT ----------

            created_at = datetime.fromisoformat(
                movement["created_at"]
            )

            india_time = created_at.astimezone(
                ZoneInfo("Asia/Kolkata")
            )

            formatted_time = india_time.strftime(
                "%d %b %Y, %I:%M %p"
            )


            st.caption(
                f"Recorded by: {recorded_by} | "
                f"Recorded at: {formatted_time}"
            )