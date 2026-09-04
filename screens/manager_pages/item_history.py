import streamlit as st
from datetime import datetime

from utils.layout import style_base_layout
from manager_services.category_service import get_categories
from manager_services.item_service import get_items
from manager_services.item_history_service import get_item_history

def item_history_page():
    style_base_layout()
    st.title("Item History")
    st.caption("Track the complete movement and activity history of your inventory.")
    st.write("")
    categories = get_categories()
    items = get_items()
   
    category_options = {
        category["name"]: category["id"]
        for category in categories
    }
    # ---------- FILTERS ----------

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
    # ITEM HISTORY
    if item_name != "Select Item":
        selected_item_id = item_options[item_name]
        item_history = get_item_history(
            selected_item_id )
        st.write("")
        # ---------- NO HISTORY ----------
        if not item_history:
            st.info(  "No history is available for this item yet.")
        else:
            st.subheader("History")
            ( type_col, quantity_col,location_col, user_col, time_col ) = st.columns([1.4, 1, 2, 1.5, 1.8])

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
            # ---------- HISTORY ROWS ----------
            for history in item_history:

                (type_col,quantity_col, location_col, user_col,time_col) = st.columns([1.4, 1, 2, 1.5, 1.8])
                movement_type = history["movement_type"]

                # ---------- TYPE ----------

                with type_col:

                    if movement_type == "receipt":

                        st.markdown( "📥 **Receipt**" )

                    elif movement_type == "issue":

                        st.markdown( "📤 **Issue**" )

                    elif movement_type == "transfer":

                        st.markdown( "🚚 **Transfer**")

                    elif movement_type == "adjustment":

                        st.markdown("🔧 **Adjustment**" )

                # ---------- QUANTITY ----------

                with quantity_col:

                    if movement_type == "receipt":

                        st.markdown( f"**+{history['quantity']:.0f}**" )

                    elif movement_type == "issue":

                        st.markdown(f"**-{history['quantity']:.0f}**")

                    elif movement_type == "adjustment":

                        adjustment_direction = (
                            history.get(
                                "adjustment_direction",
                                ""
                            ) )

                        if adjustment_direction == "increase":

                            st.markdown( f"**+{history['quantity']:.0f}**")
                        else:

                            st.markdown(f"**-{history['quantity']:.0f}**")
                    else:

                        st.markdown(f"**{history['quantity']:.0f}**")
                # ---------- LOCATION / ROUTE ----------

                with location_col:

                    if movement_type == "transfer":
                        source_location = (
                            history.get(
                                "source_location_name", "-") )

                        destination_location = (
                            history.get( "destination_location_name", "-" ))

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

                    st.write(
                        history.get(
                            "performed_by",
                            "-"
                        )
                    )

                # ---------- TIME ----------

                with time_col:

                    created_at = datetime.fromisoformat(
                        history["created_at"].replace(
                            "Z",
                            "+00:00"
                        )
                    )

                    st.write(
                        created_at.strftime(
                            "%d %b %Y, %I:%M %p"
                        )
                    )

                st.divider()