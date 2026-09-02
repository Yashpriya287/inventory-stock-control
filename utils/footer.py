import streamlit as st


def render_footer():
    st.markdown("""
        <div class="app-footer">
            Secure access to your inventory workspace
        </div>
    """, unsafe_allow_html=True)