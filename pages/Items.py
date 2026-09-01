import streamlit as st
from utils.layout import show_page_header


show_page_header(
    "Items",
    "Manage and track your inventory items"
)

col1, col2 = st.columns([3, 1],vertical_alignment="bottom")

with col1:
    search = st.text_input("Search",placeholder="Search by SKU or item name"
    )

with col2:
    st.write("")
    st.button("Add Item", type="primary")

st.subheader("Filters")

col1, col2, col3 = st.columns(3)

with col1:
    st.selectbox("Category", ["All Categories"])

with col2:
    st.selectbox("Location", ["All Locations"])

with col3:
    st.selectbox(
        "Status",
        ["Active", "Archived", "Low Stock"]
    )

st.divider()

st.info("Items will appear here once the database is connected.")