import streamlit as st

from utils.layout import style_base_layout


def staff_dashboard_page():

    style_base_layout()

    # ---------- CURRENT USER ----------

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in first.")
        return

    # ---------- HEADER ----------

    st.title("Staff Dashboard")

    st.caption(
        f"Welcome back, {current_user['full_name']} 👋"
    )

    st.write(
        "Manage stock movements across your assigned locations."
    )

    st.write("")

    # ---------- SUMMARY CARDS ----------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "📍 **Assigned Locations**\n\n"
            "Coming next"
        )

    with col2:
        st.info(
            "📦 **Today's Movements**\n\n"
            "Coming next"
        )

    with col3:
        st.info(
            "⚠️ **Low Stock Items**\n\n"
            "Coming next"
        )

    st.write("")
    st.divider()

    # ---------- QUICK ACTIONS ----------

    st.subheader("Quick Actions")

    action_col1, action_col2, action_col3 = st.columns(3)

    with action_col1:

        if st.button(
            "📥 Record Receipt",
            use_container_width=True
        ):
            st.session_state[
                "staff_selected_page"
            ] = "↔️  Stock Movements"

            st.session_state[
                "staff_movement_type"
            ] = "Receipt"

            st.rerun()

    with action_col2:

        if st.button(
            "📤 Record Issue",
            use_container_width=True
        ):
            st.session_state[
                "staff_selected_page"
            ] = "↔️  Stock Movements"

            st.session_state[
                "staff_movement_type"
            ] = "Issue"

            st.rerun()

    with action_col3:

        if st.button(
            "🔄 Transfer Stock",
            use_container_width=True
        ):
            st.session_state[
                "staff_selected_page"
            ] = "↔️  Stock Movements"

            st.session_state[
                "staff_movement_type"
            ] = "Transfer"

            st.rerun()

    st.write("")
    st.divider()

    # ---------- RECENT ACTIVITY ----------

    st.subheader("Recent Activity")

    st.info(
        "Recent stock movements will appear here."
    )

    # ---------- LOW STOCK ----------

    st.write("")
    st.subheader("Low Stock Alerts")

    st.info(
        "Low stock items from your assigned locations "
        "will appear here."
    )