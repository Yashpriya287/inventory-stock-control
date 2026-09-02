import streamlit as st

from utils.layout import (
    style_base_layout,
    style_background_home
)
from utils.header import render_header
from utils.footer import render_footer

def role_selection_screen():

    # Apply shared styling
    style_base_layout()
    style_background_home()

    # Page-specific styling
    st.markdown("""
<style>

.block-container {
    max-width: 1000px;
    padding-top: 4rem;
    padding-bottom: 2rem;
}






.role-heading {
    text-align: center;
    margin-bottom: 2rem;
}

.role-heading h2 {
    color: #F8FAFC;
    font-family: 'Outfit', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700;
    margin-bottom: 0.5rem !important;
}

.role-heading p {
    color: #94A3B8;
    font-size: 1rem;
}


.role-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.role-title {
    font-family: 'Outfit', sans-serif;
    color: #F8FAFC;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
}

.role-description {
    font-family: 'Outfit', sans-serif;
    color: #94A3B8;
    font-size: 0.95rem;
    line-height: 1.6;
}

div[data-testid="stColumn"] button {
    width: 100%;
    margin-top: -1rem;
}

.security-text {
    text-align: center;
    color: #64748B;
    font-family: 'Outfit', sans-serif;
    font-size: 0.85rem;
    margin-top: 3.5rem;
}

</style>
""", unsafe_allow_html=True)


    # Brand
    render_header()


    # Heading
    st.markdown("""
<div class="role-heading">

<h3>Select your role to continue</h3>
</div>
""", unsafe_allow_html=True)


    manager_col, staff_col = st.columns(2, gap="large")


    with manager_col:

        with st.container(border=True):

            st.markdown("<div class='role-icon'>👔</div>", unsafe_allow_html=True)
            st.header("Manager")
            st.write(
                "Manage inventory, locations, items, users, "
                "and monitor overall stock activity."
            )
            if st.button(
                "Continue as Manager →",
                key="manager_button",
                type="primary",
                use_container_width=True
            ):
                st.session_state["login_type"] = "manager"
                st.rerun()


    with staff_col:

        with st.container(border=True):

            st.markdown("<div class='role-icon'>🧑‍🔧</div>", unsafe_allow_html=True)
            st.header("Staff")
            st.write(
                "Manage stock movements and inventory "
                "at your assigned locations."
            )
            if st.button(
                "Continue as Staff →",
                key="staff_button",
                type="primary",
                use_container_width=True
            ):
                st.session_state["login_type"] = "staff"
                st.rerun()
    # Footer
    render_footer()