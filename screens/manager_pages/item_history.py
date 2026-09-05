import streamlit as st
from utils.time_utils import format_ist

from utils.layout import style_base_layout
from manager_services.category_service import get_categories
from manager_services.item_service import get_items
from manager_services.item_history_service import get_item_history


def format_value(value):
    """Convert JSONB values into a simple display string."""
    if value is None:
        return "-"

    if isinstance(value, dict):
        return str(value.get("name", value))

    return str(value)


def item_history_page():

    style_base_layout()

    st.title("Item History")
    st.caption(
        "Track the complete movement and activity history of your inventory."
    )

    st.write("")

    # ==================================================
    # GET DATA
    # ==================================================

    categories = get_categories()
    items = get_items()

    category_options = {
        category["name"]: category["id"]
        for category in categories
    }

    # ==================================================
    # FILTERS
    # ==================================================

    filter_col, _ = st.columns([1, 2])

    with filter_col:

        category_name = st.selectbox(
            "Category",
            ["Select Category"] + list(category_options.keys())
        )

        item_name = "Select Item"

        if category_name != "Select Category":

            selected_category_id = category_options[category_name]

            filtered_items = [
                item
                for item in items
                if item["category_id"] == selected_category_id
            ]

            item_options = {
                item["name"]: item["id"]
                for item in filtered_items
            }

            item_name = st.selectbox(
                "Item",
                ["Select Item"] + list(item_options.keys())
            )

    # ==================================================
    # HISTORY
    # ==================================================

    if item_name != "Select Item":

        selected_item_id = item_options[item_name]

        item_history = get_item_history(
            selected_item_id
        )

        st.write("")

        if not item_history:

            st.info(
                "No history is available for this item yet."
            )

        else:

            # ==================================================
            # ITEM ACTIVITY
            # ==================================================

            activity_history = [
                history
                for history in item_history
                if history.get("history_type") == "activity"
            ]

            if activity_history:

                st.subheader("Item Activity")

                for history in activity_history:

                    event_type = history.get(
                        "event_type",
                        ""
                    )

                    performed_by = history.get(
                        "performed_by",
                        "-"
                    )

                    performed_by_role = history.get(
                        "performed_by_role",
                        "-"
                    )

                    # ---------- CREATED ----------

                    if event_type == "created":

                        st.markdown(
                            "🟢 **Item Created**"
                        )

                        st.caption(
                            f"Created by: "
                            f"**{performed_by}** "
                            f"({performed_by_role})"
                        )

                    # ---------- FIELD CHANGED ----------

                    elif event_type == "field_changed":

                        field_name = history.get(
                            "field_name",
                            "Field"
                        )

                        old_value = format_value(
                            history.get("old_value")
                        )

                        new_value = format_value(
                            history.get("new_value")
                        )

                        field_display_names = {
                            "name": "Name",
                            "category": "Category",
                            "reorder_level": "Reorder Level"
                        }

                        display_name = (
                            field_display_names.get(
                                field_name,
                                field_name.replace(
                                    "_",
                                    " "
                                ).title()
                            )
                        )

                        if field_name == "name":

                            icon = "✏️"

                        elif field_name == "category":

                            icon = "🏷️"

                        elif field_name == "reorder_level":

                            icon = "🔢"

                        else:

                            icon = "✏️"

                        st.markdown(
                            f"{icon} **{display_name} Changed**"
                        )

                        st.write(
                            f"**{old_value} → {new_value}**"
                        )

                        st.caption(
                            f"Changed by: "
                            f"**{performed_by}** "
                            f"({performed_by_role})"
                        )

                    # ---------- STAFF NOTE ----------

                    elif event_type == "note":

                        st.markdown(
                            "📝 **Staff Note**"
                        )

                        st.write(
                            history.get(
                                "note",
                                "-"
                            )
                        )

                        st.caption(
                            f"Added by: "
                            f"**{performed_by}** "
                            f"({performed_by_role})"
                        )

                    # ---------- FALLBACK ----------

                    else:

                        st.markdown(
                            f"📌 **{event_type.replace('_', ' ').title()}**"
                        )

                        if history.get("note"):

                            st.write(
                                history["note"]
                            )

                        st.caption(
                            f"Performed by: "
                            f"**{performed_by}** "
                            f"({performed_by_role})"
                        )

                    # ---------- TIME ----------

                    st.caption(
                        format_ist(
                            history["created_at"]
                        )
                    )

                    st.divider()

            # ==================================================
            # STOCK MOVEMENT HISTORY
            # ==================================================

            movement_history = [
                history
                for history in item_history
                if history.get("history_type") == "movement"
            ]

            if movement_history:

                st.subheader("Stock Movement History")

                (
                    type_col,
                    quantity_col,
                    location_col,
                    user_col,
                    time_col
                ) = st.columns(
                    [1.4, 1, 2, 1.5, 1.8]
                )

                with type_col:
                    st.caption("Type")

                with quantity_col:
                    st.caption("Quantity")

                with location_col:
                    st.caption("Location / Route")

                with user_col:
                    st.caption("Performed By")

                with time_col:
                    st.caption("Time")

                st.divider()

                # ==================================================
                # MOVEMENT ROWS
                # ==================================================

                for history in movement_history:

                    (
                        type_col,
                        quantity_col,
                        location_col,
                        user_col,
                        time_col
                    ) = st.columns(
                        [1.4, 1, 2, 1.5, 1.8]
                    )

                    movement_type = history.get(
                        "movement_type",
                        ""
                    )

                    # ---------- TYPE ----------

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
                                "🚚 **Transfer**"
                            )

                        elif movement_type == "adjustment":

                            st.markdown(
                                "🔧 **Adjustment**"
                            )

                        else:

                            st.markdown(
                                f"**{movement_type.capitalize()}**"
                            )

                    # ---------- QUANTITY ----------

                    with quantity_col:

                        quantity = float(
                            history.get(
                                "quantity",
                                0
                            )
                        )

                        if movement_type == "receipt":

                            st.markdown(
                                f"**+{quantity:.0f}**"
                            )

                        elif movement_type == "issue":

                            st.markdown(
                                f"**-{quantity:.0f}**"
                            )

                        elif movement_type == "adjustment":

                            adjustment_direction = (
                                history.get(
                                    "adjustment_direction",
                                    ""
                                )
                            )

                            if adjustment_direction == "increase":

                                st.markdown(
                                    f"**+{quantity:.0f}**"
                                )

                            else:

                                st.markdown(
                                    f"**-{quantity:.0f}**"
                                )

                        else:

                            st.markdown(
                                f"**{quantity:.0f}**"
                            )

                    # ---------- LOCATION / ROUTE ----------

                    with location_col:

                        if movement_type == "transfer":

                            source_location = history.get(
                                "source_location_name",
                                "-"
                            )

                            destination_location = history.get(
                                "destination_location_name",
                                "-"
                            )

                            st.write(
                                f"{source_location} → "
                                f"{destination_location}"
                            )

                        else:

                            st.write(
                                history.get(
                                    "location_name",
                                    "-"
                                )
                            )

                    # ---------- PERFORMED BY ----------

                    with user_col:

                        performed_by = history.get(
                            "performed_by",
                            "-"
                        )

                        performed_by_role = history.get(
                            "performed_by_role",
                            "-"
                        )

                        st.write(
                            performed_by
                        )

                        if performed_by_role != "-":

                            st.caption(
                                performed_by_role
                            )

                    # ---------- TIME ----------

                    with time_col:

                       st.write(
                        format_ist(
                            history["created_at"]
                        )
                    )

                    st.divider()