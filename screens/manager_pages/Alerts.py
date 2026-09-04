import streamlit as st

from utils.layout import style_base_layout
from services.stock_service import get_low_stock_alerts


def low_stock_alerts_page():

    style_base_layout()

    # ---------- HEADER ----------

    st.title("Low Stock Alerts")
    st.caption(
        "Items that require attention based on their current stock levels."
    )

    st.write("")

    # ---------- GET ALERTS ----------

    low_stock_alerts = get_low_stock_alerts()

    # ---------- NO ALERTS ----------

    if not low_stock_alerts:

        st.success(
            "All items are currently stocked above their reorder levels."
        )

    else:

        # ---------- TABLE HEADER ----------

        (
            item_col,
            location_col,
            available_col,
            reorder_col,
            status_col
        ) = st.columns([2, 1.5, 1.2, 1.4, 1.5])

        with item_col:
            st.markdown(
                "<span style='font-size:16px'><b>Item</b></span>",
                unsafe_allow_html=True
            )

        with location_col:
            st.markdown(
                "<span style='font-size:16px'><b>Location</b></span>",
                unsafe_allow_html=True
            )

        with available_col:
            st.markdown(
                "<span style='font-size:16px'><b>Available</b></span>",
                unsafe_allow_html=True
            )

        with reorder_col:
            st.markdown(
                "<span style='font-size:16px'><b>Reorder Level</b></span>",
                unsafe_allow_html=True
            )

        with status_col:
            st.markdown(
                "<span style='font-size:16px'><b>Status</b></span>",
                unsafe_allow_html=True
            )

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
                        f"<b>{alert['Item']}</b></span>",
                        unsafe_allow_html=True
                    )
   

            # ---------- LOCATION ----------

            with location_col:

                st.markdown(
                    f"<span style='font-size:17px'>"
                    f"{alert['Location']}</span>",
                    unsafe_allow_html=True
                )

            # ---------- AVAILABLE ----------

            with available_col:

                st.markdown(
                    f"<span style='font-size:17px'><b>"
                    f"{alert['Available']:.0f}</b></span>",
                    unsafe_allow_html=True
                )

            # ---------- REORDER LEVEL ----------

            with reorder_col:

                st.markdown(
                    f"<span style='font-size:17px'>"
                    f"{alert['Reorder Level']:.0f}</span>",
                    unsafe_allow_html=True
                )

            # ---------- STATUS ----------

            with status_col:

                if alert["Status"] == "Out of Stock":

                    st.markdown(
                        "<span style='font-size:17px'>"
                        "🚨 Out of Stock</span>",
                        unsafe_allow_html=True
                    )

                elif alert["Status"] == "Critical Stock":

                    st.markdown(
                        "<span style='font-size:17px'>"
                        "🔶 Critical Stock</span>",
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        "<span style='font-size:17px'>"
                        "⚠️ Low Stock</span>",
                        unsafe_allow_html=True
                    )

            st.divider()