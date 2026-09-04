import streamlit as st
from manager_services.item_service import create_item, get_items, update_item,update_item_status
from utils.layout import style_base_layout
from manager_services.category_service import get_categories
from manager_services.stock_service import get_available_stock_by_item
def items_page():
    style_base_layout()
    if "show_add_item_form" not in st.session_state:
        st.session_state.show_add_item_form = False

    if "editing_item_id" not in st.session_state:
        st.session_state.editing_item_id = None    

    # Open Add Item form from Dashboard
    if st.session_state.get("dashboard_action") == "add_item":
        st.session_state.show_add_item_form = True
        st.session_state.pop("dashboard_action")

    categories = get_categories()  
    active_categories = [
            category
            for category in categories
            if category["is_active"]
        ]   
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

        # ---------- ROW 1 ----------

        sku_col, gap1, name_col,gap2 = st.columns([1, 0.12, 1,1])

        with sku_col:

            sku = st.text_input(
                "SKU",
                placeholder="e.g. ITM-001"
            )

        with name_col:

            name = st.text_input(
                "Item Name",
                placeholder="Enter item name"
            )

        # ---------- ROW 2 ----------

        category_col, gap1, reorder_col,gap2 = st.columns(
            [2, 0.18, 1,1]
        )

        with category_col:

            category_options = {
                category["name"]: category["id"]
                for category in active_categories
            }

            category_name = st.selectbox(
                "Category",
                ["Select Category"] + list(
                    category_options.keys()
                )
            )

        with reorder_col:

            reorder_level = st.number_input(
                "Reorder Level",
                min_value=0.0,
                value=0.0,
                step=1.0
            )

        # ---------- BUTTONS ----------

        st.write("")

        cancel_col, save_col, _ = st.columns(
            [1, 1, 2]
        )

        with cancel_col:

            if st.button(
                "Cancel",
                use_container_width=True
            ):

                st.session_state.show_add_item_form = False
                st.rerun()

        with save_col:

            if st.button(
                "Save Item",
                use_container_width=True
            ):

                if (
                    not sku
                    or not name
                    or category_name == "Select Category"
                ):

                    st.error(
                        "Please fill in all required fields and select a category."
                    )

                else:

                    try:

                        category_id = category_options[
                            category_name
                        ]

                        create_item(
                            sku=sku,
                            name=name,
                            description=None,
                            unit_of_measure="Piece",
                            reorder_level=reorder_level,
                            category_id=category_id
                        )

                        st.session_state.show_add_item_form = False
                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Error adding item: {repr(e)}"
                        )

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

    headers = st.columns([1, 2, 1.25, 1, 1.2, 1, 0.6])

    for col, text in zip(headers, [
        "SKU",
        "ITEM NAME",
        "CATEGORY",
        "AVAILABLE STOCK",
        "REORDER LEVEL",
        "STATUS",
        "ACTIONS"
    ]):
        col.markdown(f"**{text}**")

    st.divider()

    # ---------- DATABASE ITEMS ----------

    items = get_items()

    available_stock_by_item = (
    get_available_stock_by_item()
    )

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

        cols = st.columns([1, 2, 1.25, 1, 1.2, 1, 0.6])

        cols[0].write(item["sku"])
        cols[1].write(item["name"])

        category_name = (
            item["categories"]["name"]
            if item.get("categories")
            else "—"
        )

        cols[2].write(category_name)
        available_stock = available_stock_by_item.get(  item["id"],0)

        cols[3].write(f"{available_stock:.0f}" )

        cols[4].write(f"{item['reorder_level']:.0f}" )

        if item["is_archived"]:
            cols[5].warning("Archived")
        else:
            cols[5].success("Active")

        with cols[6]:

            with st.popover("•••", use_container_width=False):
                if st.button("✏️ Edit",key=f"edit_item_{item['id']}"):
                    st.session_state.editing_item_id = item["id"]
                    st.rerun()

                if item["is_archived"]:

                    if st.button( "Unarchive",key=f"unarchive_item_{item['id']}" ):
                        try:
                            update_item_status(  item["id"],False )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error updating item: {e}")

                else:

                    if st.button( "Archive",key=f"archive_item_{item['id']}"):
                        try:
                            update_item_status( item["id"], True )
                            st.rerun()

                        except Exception as e:
                            st.error(f"Error updating item: {e}")
    # ---------- EDIT ITEM FORM ----------

    if st.session_state.editing_item_id:
        editing_item = next(( item for item in get_items() if item["id"] == st.session_state.editing_item_id ),None)

        if editing_item:

            st.subheader("Edit Item")

            st.info(f"Editing: {editing_item['name']}")
            # ---------- ROW 1 ----------
            sku_col, gap1, name_col = st.columns(
                    [1, 0.08, 2]
                )
            with sku_col:
                edit_sku = st.text_input( "SKU", value=editing_item["sku"], key=f"edit_sku_{editing_item['id']}")

            with name_col:
                edit_name = st.text_input( "Item Name", value=editing_item["name"], key=f"edit_name_{editing_item['id']}")

            # ---------- ROW 2 ----------
            category_col, gap3, reorder_col, empty_col = st.columns(
                [2, 0.08, 1, 1])

            with category_col:

                edit_category_options = {
                    category["name"]: category["id"]
                    for category in active_categories }

                edit_category_names = list(edit_category_options.keys())
                current_category_id = editing_item.get("category_id")
                current_category_name = next(
                    (
                        name
                        for name, category_id in edit_category_options.items()
                        if category_id == current_category_id ),
                    None
                )

                if current_category_name in edit_category_names:
                    category_index = edit_category_names.index(
                        current_category_name
                    )
                else:
                    category_index = 0

                edit_category_name = st.selectbox( "Category", edit_category_names, index=category_index, key=f"edit_category_{editing_item['id']}")

            with reorder_col:
                edit_reorder_level = st.number_input(  "Reorder Level",  min_value=0.0, value=float(editing_item["reorder_level"]), step=1.0, key=f"edit_reorder_{editing_item['id']}" )

            # ---------- BUTTONS ----------
            st.write("")

            cancel_col, save_col, _ = st.columns([1, 1, 2])

            with cancel_col:
                if st.button( "Cancel Edit",  use_container_width=True, key=f"cancel_edit_{editing_item['id']}" ):
                    st.session_state.editing_item_id = None
                    st.rerun()

            with save_col:
                if st.button(  "Save Changes",  use_container_width=True,  type="primary",  key=f"save_edit_{editing_item['id']}" ):

                    if not edit_sku or not edit_name:
                        st.error("Please fill in all required fields.")

                    else:
                        try:

                            edit_category_id = edit_category_options[
                                edit_category_name
                            ]

                            update_item(
                                item_id=editing_item["id"],
                                sku=edit_sku.strip(),
                                name=edit_name.strip(),
                                reorder_level=edit_reorder_level,
                                category_id=edit_category_id
                            )

                            st.session_state.editing_item_id = None
                            st.success("Item updated successfully!")
                            st.rerun()

                        except Exception as e:
                            st.error(f"Error updating item: {repr(e)}")

        st.divider()
    