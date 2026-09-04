import streamlit as st

from utils.layout import style_base_layout


def staff_items_page():

    style_base_layout()

    # ---------- HEADER ----------

    st.title("Items")

    st.caption(
        "View inventory items and their current stock status."
    )

    st.write("")

    # ---------- SEARCH AND FILTERS ----------

    search_col, category_col = st.columns([2, 1])

    with search_col:

        st.text_input(
            "Search Items",
            placeholder="🔍 Search by item name or SKU",
            label_visibility="collapsed",
            disabled=True
        )

    with category_col:

        st.selectbox(
            "Category",
            ["All Categories"],
            label_visibility="collapsed",
            disabled=True
        )

    st.write("")

    # ---------- TABLE ----------

    st.subheader("Items")

    headers = st.columns(
        [2, 1.5, 1.2, 1.2, 1.3]
    )

    header_names = [
        "ITEM",
        "CATEGORY",
        "UNIT",
        "AVAILABLE STOCK",
        "STATUS"
    ]

    for col, text in zip(headers, header_names):

        with col:

            st.markdown(f"**{text}**")

    st.divider()

    # ---------- EMPTY STATE ----------

    st.info(
        "Items will appear here once the page is connected "
        "to the inventory database."
    )