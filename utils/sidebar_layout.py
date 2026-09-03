import streamlit as st


def sidebar_base_layout():

    st.markdown("""
    <style>

    /* =========================================
       SIDEBAR
    ========================================= */

    [data-testid="stSidebar"] {
        min-width: 340px !important;
        max-width: 340px !important;
        width: 340px !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        width: 340px !important;
        min-width: 340px !important;

        background: radial-gradient(
            circle at top left,
            #202b48,
            #111a2d 70%
        ) !important;

        border-right: 1px solid rgba(130, 150, 210, 0.35) !important;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 1.2rem 1rem !important;
    }

    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }


    /* =========================================
       DIVIDERS
    ========================================= */

    [data-testid="stSidebar"] hr {
        border: none !important;
        border-top: 1px solid rgba(130, 150, 190, 0.16) !important;
        margin: 1rem 0 !important;
    }


    /* =========================================
       PROFILE
    ========================================= */

    .profile-name {
        color: #f4f5f7 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.2rem !important;
    }

    .manager-role {
        color: #62d59a !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.3rem !important;
    }

    .online-status {
        display: inline-block !important;
        color: #63e39b !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        background: rgba(35, 160, 90, 0.14) !important;
        padding: 0.2rem 0.55rem !important;
        border-radius: 20px !important;
    }


    /* =========================================
       NAVIGATION TITLE
    ========================================= */

    .nav-title {
        color: #8995aa !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px !important;
        margin: 1rem 0 0.7rem !important;
    }


    /* =========================================
       RADIO NAVIGATION
    ========================================= */

    /* Hide Navigation label */

    [data-testid="stSidebar"] .stRadio > label {
        display: none !important;
    }


    /* Spacing between navigation items */

    [data-testid="stSidebar"]
    .stRadio div[role="radiogroup"] {
        gap: 0.25rem !important;
    }


    /* -----------------------------------------
       REMOVE THE WHITE / RED RADIO DOTS
    ----------------------------------------- */

    /* Hide input */

    [data-testid="stSidebar"]
    .stRadio input[type="radio"] {
        display: none !important;
    }


    /*
       Hide the Streamlit / BaseWeb radio
       indicator containing the radio input
    */

    [data-testid="stSidebar"]
    .stRadio div:has(> input[type="radio"]) {
        display: none !important;
    }


    /*
       Alternative Streamlit radio indicator
    */

    [data-testid="stSidebar"]
    .stRadio [data-baseweb="radio"] > div:first-child {
        display: none !important;
    }


    /* -----------------------------------------
       NAVIGATION ITEM
    ----------------------------------------- */

    [data-testid="stSidebar"]
    .stRadio div[role="radiogroup"] label {
        display: flex !important;
        align-items: center !important;

        padding: 0.65rem 0.8rem !important;

        min-height: 42px !important;

        /* Sharp corners */
        border-radius: 0 !important;

        transition: 0.2s ease !important;
    }


    /* Navigation text */

    [data-testid="stSidebar"]
    .stRadio label p {
        color: #d5d9e2 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }


    /* Hover */

    [data-testid="stSidebar"]
    .stRadio label:hover {
        background: rgba(120, 130, 255, 0.12) !important;
    }


    /* -----------------------------------------
       SELECTED NAVIGATION
    ----------------------------------------- */

    [data-testid="stSidebar"]
    .stRadio label:has(input[type="radio"]:checked) {
        background: linear-gradient(
            90deg,
            #4c5bd5,
            #5f5bdc
        ) !important;

        border-radius: 0 !important;

        box-shadow: 0 5px 15px rgba(
            70,
            80,
            220,
            0.25
        ) !important;
    }


    [data-testid="stSidebar"]
    .stRadio label:has(input[type="radio"]:checked) p {
        color: white !important;
        font-weight: 600 !important;
    }


    /* =========================================
       LOGOUT BUTTON
    ========================================= */

    [data-testid="stSidebar"]
    button[kind="secondary"] {
        background: rgba(
            150,
            35,
            45,
            0.22
        ) !important;

        border: 1px solid rgba(
            235,
            75,
            80,
            0.42
        ) !important;

        color: #ff8585 !important;

        border-radius: 12px !important;

        min-height: 2.7rem !important;

        font-size: 1rem !important;
        font-weight: 600 !important;
    }


    [data-testid="stSidebar"]
    button[kind="secondary"]:hover {
        background: rgba(
            180,
            40,
            50,
            0.30
        ) !important;

        border-color: #f05b63 !important;
    }


    /* =========================================
       FOOTER
    ========================================= */

    .sidebar-footer {
        color: #8894a8 !important;
        font-size: 0.8rem !important;
        text-align: center !important;
        line-height: 1.8 !important;
    }

    </style>
    """, unsafe_allow_html=True)