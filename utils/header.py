import streamlit as st


def render_header():
    # Main centered header area
    left, center, right = st.columns([1.4, 3, 1.4])

    with center:
        # Box + BUSY in one row
        icon_col, text_col = st.columns([1, 3.5], gap="small",vertical_alignment="center")

        with icon_col:
            st.image(
                "assets/box_logoo.png",
                width=100
            )

        with text_col:

            st.title("BUSY")
            st.caption("Inventory & Stock Control System")
                
            
