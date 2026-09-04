import streamlit as st

from utils.layout import style_base_layout

from manager_services.category_service import get_categories

from manager_services.stock_service import  get_stock_overview



def stock_overview_page():

    style_base_layout()

    # ---------- HEADER ----------

    st.title("Stock Overview")

    st.caption(
        "View current inventory across all locations."
    )

    st.write("")

    # ---------- GET ACTIVE CATEGORIES ----------

    categories = get_categories()

    active_categories = [
        category
        for category in categories
        if category["is_active"]
    ]

    category_options = {
        category["name"]: category["id"]
        for category in active_categories
    }

    # ---------- CATEGORY FILTER ----------

    filter_col, _ = st.columns([1, 2])

    with filter_col:

        selected_category = st.selectbox(
            "Category",
            ["All Categories"] +
            list(category_options.keys())
        )

    # ---------- GET STOCK ----------

    if selected_category == "All Categories":

        stock_overview = get_stock_overview()

    else:

        category_id = category_options[
            selected_category
        ]

        stock_overview = get_stock_overview(
            category_id
        )

    # ---------- STOCK TABLE ----------

    st.write("")

    if not stock_overview:

        st.info(
            "No stock records found for this category."
        )

    else:

        # ---------- TABLE HEADER ----------

        header_item, header_location, header_stock, header_status = st.columns(
            [2.2, 2, 1.5, 1.5]
        )

        with header_item:
            st.caption("Item")

        with header_location:
            st.caption("Location")

        with header_stock:
            st.caption("Available Stock")

        with header_status:
            st.caption("Status")

        st.divider()

        # ---------- STOCK ROWS ----------

        for stock in stock_overview:

            item_col, location_col, quantity_col, status_col = st.columns(
                [2.2, 2, 1.5, 1.5]
            )

            with item_col:
                st.write(stock["Item"])

            with location_col:
                st.write(stock["Location"])

            with quantity_col:
                st.markdown(
        f'**{stock["Available Stock"]:.0f}**'
                     )
            with status_col:

                if stock["Status"] == "In Stock":
                    st.write("In Stock")

                elif stock["Status"] == "Low Stock":
                    st.write("⚠️ Low Stock")

                else:
                    st.write("Out of Stock")

            st.divider()