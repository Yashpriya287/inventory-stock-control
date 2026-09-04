import streamlit as st

from utils.layout import style_base_layout

from staff_services.staff_item_service import (
    get_staff_items
)


def staff_items_page():

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

    # ==================================================
    # HEADER
    # ==================================================

    st.title("Items")

    st.caption(
        "View active inventory items and their details."
    )

    st.write("")

    # ==================================================
    # GET STAFF ITEMS
    # ==================================================

    items = get_staff_items()

    # ==================================================
    # GET CATEGORY OPTIONS
    # ==================================================

    category_names = sorted({

        item["category_name"]

        for item in items

        if item["category_name"]

    })

    category_options = [

        "All Categories"

    ] + category_names

    # ==================================================
    # SEARCH AND FILTERS
    # ==================================================

    search_col,empty, category_col = st.columns(
        [0.6,0.22, 0.7]
    )

    with search_col:

        search = st.text_input(

            "Search Items",

            placeholder="🔍 Search by item name or SKU",

            label_visibility="collapsed"

        )

    with category_col:

        selected_category = st.selectbox(

            "Category",

            category_options,

            label_visibility="collapsed"

        )

    # ==================================================
    # APPLY SEARCH FILTER
    # ==================================================

    if search:

        search = search.lower().strip()

        items = [

            item

            for item in items

            if search in item["name"].lower()

            or search in item["sku"].lower()

        ]

    # ==================================================
    # APPLY CATEGORY FILTER
    # ==================================================

    if selected_category != "All Categories":

        items = [

            item

            for item in items

            if item["category_name"]
            == selected_category

        ]

    st.write("")

    # ==================================================
    # TABLE
    # ==================================================

    st.subheader("Items")

    headers = st.columns(

        [2, 1.5, 1.2]

    )

    header_names = [

        "ITEM",

        "CATEGORY",

        "REORDER LEVEL"

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

    if not items:

        st.info(
            "No items found."
        )

        return

    # ==================================================
    # ITEM ROWS
    # ==================================================

    for item in items:

        (

            item_col,

            category_col,

            reorder_col

        ) = st.columns(

            [2, 1.5, 1.2]

        )

        # ---------- ITEM ----------

        with item_col:

            st.write(
                item["name"]
            )

            st.caption(
                item["sku"]
            )

        # ---------- CATEGORY ----------

        with category_col:

            st.write(
                item["category_name"]
            )

        # ---------- REORDER LEVEL ----------

        with reorder_col:

            st.write(
                f"{item['reorder_level']:g}"
            )

        st.divider()