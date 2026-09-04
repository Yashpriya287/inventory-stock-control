import streamlit as st

from utils.layout import style_base_layout

from staff_services.staff_low_stock_service import (
    get_staff_low_stock_alerts
)

def staff_low_stock_alert_page():

    style_base_layout()

    # ---------- CURRENT USER ----------

    current_user = st.session_state.get("user")

    if not current_user:

        st.warning("Please log in first.")

        return

    staff_id = current_user["id"]

    # ---------- HEADER ----------

    st.title("Low Stock Alerts")

    st.caption(
        "Items at your assigned locations that require attention."
    )

    st.write("")

    # ---------- GET ALERTS ----------

    low_stock_alerts = get_staff_low_stock_alerts(
        staff_id
    )

    # ---------- NO ALERTS ----------

    if not low_stock_alerts:

        st.success(
            "No low stock alerts at your assigned locations."
        )

        return

    # ---------- TABLE HEADER ----------

    (
        item_col,
        location_col,
        available_col,
        reorder_col,
        status_col
    ) = st.columns([2, 1.5, 1.2, 1.4, 1.5])

    with item_col:

        st.markdown("**ITEM**")

    with location_col:

        st.markdown("**LOCATION**")

    with available_col:

        st.markdown("**AVAILABLE**")

    with reorder_col:

        st.markdown("**REORDER LEVEL**")

    with status_col:

        st.markdown("**STATUS**")

    st.divider()

    # ---------- ALERT ROWS ----------

    for alert in low_stock_alerts:

        (
            item_col,
            location_col,
            available_col,
            reorder_col,
            status_col
        ) = st.columns([2, 1.5, 1.2, 1.4, 1.5])

        # ---------- ITEM ----------

        with item_col:

            st.markdown(
                f"<b>{alert['Item']}</b>",
                unsafe_allow_html=True
            )

        # ---------- LOCATION ----------

        with location_col:

            st.write(
                alert["Location"]
            )

        # ---------- AVAILABLE ----------

        with available_col:

            st.markdown(
                f"**{alert['Available']:.0f}**"
            )

        # ---------- REORDER LEVEL ----------

        with reorder_col:

            st.write(
                f"{alert['Reorder Level']:.0f}"
            )

        # ---------- STATUS ----------

        with status_col:

            if alert["Status"] == "Out of Stock":

                st.markdown(
                    "🚨 **Out of Stock**"
                )

            elif alert["Status"] == "Critical Stock":

                st.markdown(
                    "🔶 **Critical Stock**"
                )

            else:

                st.markdown(
                    "⚠️ **Low Stock**"
                )

        st.divider()