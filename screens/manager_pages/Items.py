import streamlit as st
from services.item_service import create_item, get_items
from utils.layout import style_base_layout
from services.category_service import get_categories
def items_page():
    style_base_layout()
    if "show_add_item_form" not in st.session_state:
        st.session_state.show_add_item_form = False

    categories = get_categories()    
    # ---------- HEADER ----------
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("Items")
        st.caption("Manage and track your inventory items.")
    with col2:
        st.write("")
        st.write("")
        if st.button("＋ Add Item", use_container_width=True):
            st.session_state.show_add_item_form = True
    st.write("")
# ---------- ADD ITEM FORM ----------

   
    if st.session_state.show_add_item_form:
        st.subheader("Add New Item")
        #  ROW 1
        sku_col, gap1, name_col, gap2, unit_col = st.columns(  [1, 0.08, 2, 0.08, 1])

        with sku_col:
            sku = st.text_input( "SKU", placeholder="e.g. ITM-001")
        with name_col:
            name = st.text_input(  "Item Name",  placeholder="Enter item name" )
        with unit_col:
            unit = st.text_input(  "Unit", placeholder="e.g. Piece")
        #  ROW 2
        category_col, gap3, reorder_col, empty_col = st.columns(  [2, 0.08, 1, 1] )

        with category_col:
            category_names = ["Select Category"] + [
                category["name"] for category in categories
            ]

            category = st.selectbox(
                "Category",
                category_names
            )

        with reorder_col:
            reorder_level = st.number_input(
                "Reorder Level",
                min_value=0.0,
                value=0.0,
                step=1.0
            )

        #  DESCRIPTION
        description_col, empty_col = st.columns([2, 2])

        with description_col:
            description = st.text_area( "Description", placeholder="Enter a short description (optional)",  height=80 )

        # ---------- BUTTONS ----------
        st.write("")
        cancel_col, save_col, _ = st.columns([1, 1, 2])

        with cancel_col:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_add_item_form = False
                st.rerun()

        with save_col:
            if st.button("Save Item", use_container_width=True):

                if not sku or not name or not unit:
                    st.error("Please fill in all required fields.")

                else:
                    try:
                        category_id = None

                        if category != "Select Category":
                            selected_category = next(
                                (
                                    category_data
                                    for category_data in categories
                                    if category_data["name"] == category
                                ),
                                None
                            )

                            if selected_category is not None:
                                category_id = selected_category["id"]

                        create_item(
                            sku=sku,
                            name=name,
                            description=description,
                            unit_of_measure=unit,
                            reorder_level=reorder_level,
                            category_id=category_id
                        )

                        st.session_state.show_add_item_form = False
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error adding item: {repr(e)}")

    st.divider()

    # ---------- FILTERS ----------

    search_col, category_col, status_col = st.columns([1.6, 0.8, 0.8])

    with search_col:
        search = st.text_input( "Search",placeholder="🔍 Search by item name or SKU", label_visibility="collapsed")

    with category_col:
        category_filter_options = ["All Categories"] + [
            category["name"] for category in categories
        ]

        category_filter = st.selectbox( "Category Filter", category_filter_options, label_visibility="collapsed")

    with status_col:
        status_filter = st.selectbox( "Status Filter",  ["All Status", "Active", "Archived"], label_visibility="collapsed" )
    # ---------- TABLE HEADER ----------

    headers = st.columns([1, 2, 1.25, 0.9, 1.2, 1, 0.6])

    for col, text in zip(headers, [
        "SKU",
        "ITEM NAME",
        "CATEGORY",
        "UNIT",
        "REORDER LEVEL",
        "STATUS",
        "ACTIONS"
    ]):
        col.markdown(f"**{text}**")

    st.divider()

    # ---------- DATABASE ITEMS ----------

    items = get_items()

    # ---------- SEARCH FILTER ----------

    if search:
        search = search.lower()

        items = [
            item for item in items
            if search in item["name"].lower()
            or search in item["sku"].lower()
        ]
    # ---------- CATEGORY FILTER ----------

    if category_filter != "All Categories":

        items = [
            item for item in items
            if item.get("categories")
            and item["categories"]["name"] == category_filter
        ]   

    # ---------- STATUS FILTER ----------
    if status_filter == "Active":
        items = [
            item for item in items
            if not item["is_archived"]
        ]

    elif status_filter == "Archived":
        items = [
            item for item in items
            if item["is_archived"]
        ]


    if not items:
        st.info("No items have been added yet.")

    for item in items:

        cols = st.columns([1, 2, 1.25, 0.9, 1.2, 1, 0.6])

        cols[0].write(item["sku"])
        cols[1].write(item["name"])

        category_name = (
            item["categories"]["name"]
            if item.get("categories")
            else "—"
        )

        cols[2].write(category_name)
        cols[3].write(item["unit_of_measure"])
        cols[4].write(item["reorder_level"])

        if item["is_archived"]:
            cols[5].warning("Archived")
        else:
            cols[5].success("Active")

        cols[6].button(
            "•••",
            key=f"action_{item['id']}"
        )

        st.divider()