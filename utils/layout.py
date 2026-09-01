import streamlit as st


def setup_page(title: str, icon: str):
    """
    Apply common configuration and layout
    to every page in the application.
    """

    st.set_page_config(
        page_title=f"{title} | Busy Inventory",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )


def show_page_header(title: str, subtitle: str = ""):
    """Display a consistent page header."""

    st.title(title)

    if subtitle:
        st.caption(subtitle)

    st.divider()