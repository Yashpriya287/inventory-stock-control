import streamlit as st
from utils.layout import style_base_layout
from services.category_service import create_category, get_categories,update_category,update_category_status

def category_page():

    style_base_layout()
    if "show_add_category_form" not in st.session_state:
        st.session_state.show_add_category_form = False

    if "editing_category_id" not in st.session_state:
        st.session_state.editing_category_id = None

    # ---------- HEADER ----------

    title_col, button_col = st.columns([4, 1])

    with title_col:
        st.title("Categories")
        st.caption("Organize and manage your inventory categories.")

    with button_col:
        st.write("")
        st.write("")

        if st.button(
            "＋ Add Category",
            use_container_width=True
        ):
            st.session_state.show_add_category_form = True

    st.write("")
    # ---------- ADD CATEGORY FORM ----------

    if st.session_state.show_add_category_form:

        st.subheader("Add New Category")

        category_col, gap, description_col = st.columns([1, 0.08, 2])

        with category_col:
            category_name = st.text_input(  "Category Name",  placeholder="e.g. Electronics" )

        with description_col:
            description = st.text_input( "Description",placeholder="Enter category description (optional)")

        st.write("")

        cancel_col, save_col, empty_col = st.columns([1, 1, 3])

        with cancel_col:
            if st.button(
                "Cancel",
                use_container_width=True,
                key="cancel_category"
            ):
                st.session_state.show_add_category_form = False
                st.rerun()

        with save_col:
            if st.button(
                "Save Category",
                use_container_width=True,
                type="primary",
                key="save_category"
            ):
                if not category_name:
                    st.error("Please enter a category name.")

                else:
                    try:
                        create_category(
                            name=category_name.strip(),
                            description=description.strip()  )
                        st.session_state.show_add_category_form = False
                        st.success("Category added successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error adding category: {e}")
        st.divider()

    # ---------- CATEGORY FILTER ----------

    categories = get_categories()

    category_options = ["All Categories"] + [
        category["name"] for category in categories
    ]

    filter_col, empty_col = st.columns([2, 3])

    with filter_col:

        selected_category_name = st.selectbox(
            "Select Category",
            category_options,
            label_visibility="collapsed"
        )

    st.write("")


    # ---------- TABLE ----------

    st.subheader("Categories")

    headers = st.columns([2, 3, 1.2, 0.7])

    for col, text in zip(
        headers,
        [
            "CATEGORY",
            "DESCRIPTION",
            "STATUS",
            "ACTIONS"
        ]
    ):
        col.markdown(f"**{text}**")

    st.divider()


    # ---------- CATEGORY FILTER ----------

    if selected_category_name != "All Categories":

        categories = [
            category
            for category in categories
            if category["name"] == selected_category_name
        ]


    # ---------- TABLE ROWS ----------

    if not categories:

        st.info("No categories found.")

    else:

        for category in categories:

            cols = st.columns([2, 3, 1.2, 0.7])

            cols[0].write(category["name"])

            cols[1].write(
                category["description"]
                if category["description"]
                else "—"
            )
            if category["is_active"]:
                cols[2].warning("Active")
            else:
                cols[2].success("Inactive")

            with cols[3]:
                with st.popover("•••"):
                    if st.button("✏️ Edit", key=f"edit_category_{category['id']}"):
                        st.session_state.editing_category_id = category["id"]
                        st.rerun()

                    if category["is_active"]:
                        if st.button("Deactivate", key=f"deactivate_category_{category['id']}"):
                            try:
                                update_category_status(
                                    category["id"],False)
                                st.rerun()

                            except Exception as e:
                                st.error(f"Error updating category: {e}")

                    else:
                        if st.button( "Activate", key=f"activate_category_{category['id']}" ):
                            try:
                                update_category_status(
                                    category["id"],
                                    True)
                                st.rerun()

                            except Exception as e:
                                st.error(f"Error updating category: {e}")
        #  EDIT CATEGORY 

        if st.session_state.editing_category_id:
            selected_category = next(
                (
                    category
                    for category in categories
                    if category["id"] == st.session_state.editing_category_id
                ),
                None
            )

            if selected_category:

                st.subheader("Edit Category")

                category_name = st.text_input( "Category Name",value=selected_category["name"], key=f"edit_category_name_{selected_category['id']}" )
                description = st.text_input( "Description",value=selected_category["description"] or "", key=f"edit_category_description_{selected_category['id']}")
                st.write("")

                cancel_col, save_col, _ = st.columns([1, 1, 3])

                with cancel_col:

                    if st.button( "Cancel Edit", use_container_width=True, key="cancel_edit_category"):
                        st.session_state.editing_category_id = None
                        st.rerun()

                with save_col:

                    if st.button( "Save Changes", type="primary",use_container_width=True, key="save_edit_category" ):

                        if not category_name.strip():
                            st.error("Please enter a category name.")

                        else:
                            try:

                                update_category(
                                    category_id=selected_category["id"],
                                    name=category_name.strip(),
                                    description=description.strip()
                                )

                                st.session_state.editing_category_id = None
                                st.success("Category updated successfully!")
                                st.rerun()

                            except Exception as e:
                                st.error(f"Error updating category: {e}")                

            st.divider()