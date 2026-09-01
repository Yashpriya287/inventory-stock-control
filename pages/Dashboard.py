from utils.layout import show_page_header
import streamlit as st


show_page_header(
    "Dashboard",
    "Overview of your inventory and stock activity"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Active Items", 0)

with col2:
    st.metric("Low Stock", 0)

with col3:
    st.metric("Today's Movements", 0)

with col4:
    st.metric("Items Moved This Week", 0)

st.divider()

st.info("Dashboard data will appear here once the database is connected.")