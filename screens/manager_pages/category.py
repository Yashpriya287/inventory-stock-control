import streamlit as st
from utils.layout import style_base_layout
from services.category_service import create_category, get_categories

def category_page():

    style_base_layout()
    if "show_add_category_form" not in st.session_state:
        st.session_state.show_add_category_form = False

    # ---------- SESSION STATE ----------

    if "show_add_category_form" not in st.session_state:
        st.session_state.show_add_category_form = False

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

    # ---------- SEARCH ----------

    search_col, empty_col = st.columns([2, 3])

    with search_col:
        search = st.text_input(
            "Search Categories",
            placeholder="🔍 Search categories",
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


    # ---------- DATABASE CATEGORIES ----------

    categories = get_categories()


    # ---------- SEARCH FILTER ----------

    if search:

        search = search.lower()

        categories = [
            category for category in categories
            if search in category["name"].lower()
            or search in (category["description"] or "").lower()
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

            # Schema currently has no is_archived column
            cols[2].success("Active")

            cols[3].button(
                "•••",
                key=f"category_action_{category['id']}"
            )

            st.divider()