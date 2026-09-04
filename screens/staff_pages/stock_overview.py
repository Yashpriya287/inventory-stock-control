import streamlit as st

from utils.layout import style_base_layout


def staff_stock_overview_page():

    style_base_layout()

    # ---------- HEADER ----------

    st.title("Stock Overview")

    st.caption(
        "View current inventory across your assigned locations."
    )

    st.write("")

    # ---------- FILTERS ----------

    filter_col1, filter_col2, filter_col3 = st.columns(
        [2, 1.5, 1]
    )

    with filter_col1:

        st.text_input(
            "Search",
            placeholder="🔍 Search by item name or SKU",
            label_visibility="collapsed",
            disabled=True
        )

    with filter_col2:

        st.selectbox(
            "Location",
            ["All Assigned Locations"],
            label_visibility="collapsed",
            disabled=True
        )

    with filter_col3:

        st.selectbox(
            "Status",
            [
                "All Status",
                "In Stock",
                "Low Stock",
                "Out of Stock"
            ],
            label_visibility="collapsed",
            disabled=True
        )

    st.write("")

    # ---------- TABLE ----------

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

    for col, text in zip(headers, header_names):

        with col:
            st.markdown(f"**{text}**")

    st.divider()

    # ---------- EMPTY STATE ----------

    st.info(
        "Stock data for your assigned locations "
        "will appear here."
    )