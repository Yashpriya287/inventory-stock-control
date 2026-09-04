import streamlit as st

from utils.layout import style_base_layout

from staff_services.staff_stock_overview_service import (
    get_staff_locations,
    get_staff_stock_overview
)


def staff_stock_overview_page():

    style_base_layout()

    # ==================================================
    # CURRENT USER
    # ==================================================

    current_user = st.session_state.get("user")

    if not current_user:

        st.warning(
            "Please log in first."
        )

        return

    staff_id = current_user["id"]

    # ==================================================
    # HEADER
    # ==================================================

    st.title("Stock Overview")

    st.caption(
        "View current inventory across your assigned locations."
    )

    st.write("")

    # ==================================================
    # GET ASSIGNED LOCATIONS
    # ==================================================

    assigned_locations = get_staff_locations(
        staff_id
    )

    if not assigned_locations:

        st.warning(
            "You have not been assigned to any locations."
        )

        return

    # ==================================================
    # LOCATION OPTIONS
    # ==================================================

    location_options = {

        "All Assigned Locations": None

    }

    for location in assigned_locations:

        location_options[
            location["name"]
        ] = location["id"]

    # ==================================================
    # FILTERS
    # ==================================================

    filter_col1, filter_col2, filter_col3 = (
        st.columns([2, 1.5, 1])
    )

    with filter_col1:

        search = st.text_input(

            "Search",

            placeholder="🔍 Search by item name or SKU",

            label_visibility="collapsed"

        )

    with filter_col2:

        selected_location_name = st.selectbox(

            "Location",

            list(location_options.keys()),

            label_visibility="collapsed"

        )

    with filter_col3:

        selected_status = st.selectbox(

            "Status",

            [
                "All Status",
                "In Stock",
                "Low Stock",
                "Out of Stock"
            ],

            label_visibility="collapsed"

        )

    selected_location_id = location_options[
        selected_location_name
    ]

    st.write("")

    # ==================================================
    # GET STOCK DATA
    # ==================================================

    stock_rows = get_staff_stock_overview(staff_id)


    # ==================================================
    # APPLY FILTERS
    # ==================================================

    # ---------- SEARCH ----------

    if search:

        search = search.lower().strip()

        stock_rows = [

            stock

            for stock in stock_rows

            if search in stock["item_name"].lower()

            or search in stock["sku"].lower()

        ]


    # ---------- LOCATION ----------

    if selected_location_id:

        stock_rows = [

            stock

            for stock in stock_rows

            if stock["location_id"] == selected_location_id

        ]


    # ---------- STATUS ----------

    if selected_status != "All Status":

        stock_rows = [

            stock

            for stock in stock_rows

            if stock["status"] == selected_status

        ]
    # ==================================================
    # TABLE
    # ==================================================

    st.subheader("Current Stock")

    headers = st.columns(
        [2, 1.5, 1.2, 1.3, 1.2]
    )

    header_names = [

        "ITEM",

        "LOCATION",

        "AVAILABLE STOCK",

        "REORDER LEVEL",

        "STATUS"

    ]

    for col, text in zip(
        headers,
        header_names
    ):

        with col:

            st.markdown(
                f"**{text}**"
            )

    st.divider()

    # ==================================================
    # EMPTY STATE
    # ==================================================

    if not stock_rows:

        st.info(
            "No stock records found for your assigned locations."
        )

        return

    # ==================================================
    # STOCK ROWS
    # ==================================================

    for stock in stock_rows:

        (
            item_col,
            location_col,
            available_col,
            reorder_col,
            status_col
        ) = st.columns(
            [2, 1.5, 1.2, 1.3, 1.2]
        )

        # ---------- ITEM ----------

        with item_col:

            st.write(
                stock["item_name"]
            )

            st.caption(
                stock["sku"]
            )

        # ---------- LOCATION ----------

        with location_col:

            st.write(
                stock["location_name"]
            )

        # ---------- AVAILABLE STOCK ----------

        with available_col:

            st.markdown(
                f"**{stock['available_stock']:g}**"
            )

        # ---------- REORDER LEVEL ----------

        with reorder_col:

             st.markdown(
                f"**{stock['reorder_level']:g}**"
            )

        # ---------- STATUS ----------

        with status_col:

            if stock["status"] == "Out of Stock":

                st.error(
                    "Out of Stock"
                )

            elif stock["status"] == "Low Stock":

                st.warning(
                    "Low Stock"
                )

            else:

                st.success(
                    "In Stock"
                )

        st.divider()