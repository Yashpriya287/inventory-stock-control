import streamlit as st

from datetime import datetime
from zoneinfo import ZoneInfo

from utils.layout import style_base_layout

from staff_services.staff_movement_services import (
    get_active_items
)

from staff_services.staff_item_history_service import (
    get_staff_item_history
)


def staff_item_history_page():

    style_base_layout()

    # ---------- CURRENT USER ----------

    current_user = st.session_state.get("user")

    if not current_user:

        st.warning("Please log in first.")

        return

    staff_id = current_user["id"]

    # ---------- HEADER ----------

    st.title("Item History")

    st.caption(
        "View stock movement history for your assigned locations."
    )

    st.write("")

    # ---------- GET ITEMS ----------

    items = get_active_items()

    if not items:

        st.info(
            "No active items available."
        )

        return

    # ---------- ITEM DROPDOWN ----------

    item_options = {

        f"{item['name']} ({item['sku']})": item

        for item in items

    }

    item_col, empty_col = st.columns([2, 3])

    with item_col:

        selected_item_name = st.selectbox(
            "Select Item",
            options=list(item_options.keys()),
            index=None,
            placeholder="Select an item"
        )

    # ---------- STOP UNTIL ITEM SELECTED ----------

    if not selected_item_name:

        st.info(
            "Select an item to view its movement history."
        )

        return

    selected_item = item_options[
        selected_item_name
    ]

    st.write("")

    # ---------- GET HISTORY ----------

    history = get_staff_item_history(

        staff_id,

        selected_item["id"]

    )

    # ---------- NO HISTORY ----------

    if not history:

        st.info(
            "No movement history found for this item "
            "at your assigned locations."
        )

        return

    # ---------- TABLE HEADER ----------

    (
        type_col,
        quantity_col,
        location_col,
        performed_col,
        date_col
    ) = st.columns([1.4, 1, 2, 1.5, 1.8])

    with type_col:

        st.markdown("**TYPE**")

    with quantity_col:

        st.markdown("**QUANTITY**")

    with location_col:

        st.markdown("**LOCATION**")

    with performed_col:

        st.markdown("**RECORDED BY**")

    with date_col:

        st.markdown("**DATE & TIME**")

    st.divider()

    # ---------- HISTORY ROWS ----------

    for movement in history:

        (
            type_col,
            quantity_col,
            location_col,
            performed_col,
            date_col
        ) = st.columns([1.4, 1, 2, 1.5, 1.8])

        movement_type = movement[
            "movement_type"
        ].lower()

        # ---------- MOVEMENT TYPE ----------

        with type_col:

            if movement_type == "receipt":

                st.markdown(
                    "📥 **Receipt**"
                )

            elif movement_type == "issue":

                st.markdown(
                    "📤 **Issue**"
                )

            elif movement_type == "transfer":

                st.markdown(
                    "↔️ **Transfer**"
                )

        # ---------- QUANTITY ----------

        with quantity_col:

            st.write(
                f"{float(movement['quantity']):.0f}"
            )

        # ---------- LOCATION ----------

        with location_col:

            if movement_type == "transfer":

                st.write(
                    f"{movement['source_location_name']} "
                    f"→ "
                    f"{movement['destination_location_name']}"
                )

            else:

                st.write(
                    movement["location_name"]
                )

        # ---------- RECORDED BY ----------

        with performed_col:

            user_role = (
                movement.get("user_role", "")
                .strip()
                .title()
            )

            st.write(
                f"{movement['performed_by']} ({user_role})"
            )

        # ---------- DATE AND TIME ----------

        with date_col:

            created_at = datetime.fromisoformat(
                movement["created_at"]
            )

            india_time = created_at.astimezone(
                ZoneInfo("Asia/Kolkata")
            )

            formatted_time = india_time.strftime(
                "%d %b %Y, %I:%M %p"
            )

            st.write(
                formatted_time
            )

        st.divider()