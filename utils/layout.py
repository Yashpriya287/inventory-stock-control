import streamlit as st


def style_background_home():
    st.markdown("""
        <style>
            .stApp {
                background:
                    radial-gradient(
                        circle at top,
                        #1F2A44 0%,
                        #0B1220 70%
                    ) !important;
            }
        </style>
    """, unsafe_allow_html=True)

def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp{
              background:#E0E3FF !important}
                                
        </style>
""", unsafe_allow_html=True)

        
def style_base_layout():
    st.markdown("""
        <style>
            @import url(
                'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap'
            );

            /*hide top baar of streamlit*/
            #MainMenu, footer, header{
                        visibility:hidden;}
                        .block-container{
                        padding-top:1.5rem}


            /* GLOBAL FONT */
            html, body, [class*="css"] {
                font-family: 'Outfit', sans-serif !important;
            }


            /* STREAMLIT TEXT */
            p, span, label, div {
                font-family: 'Outfit', sans-serif !important;
            }


            /* MAIN HEADING */
            h1 {
                font-family: 'Outfit', sans-serif !important;
                font-size: 3.5rem !important;
                font-weight: 800 !important;
                line-height: 1.1 !important;
                color: #F7F3EE !important;
                margin-bottom: 0.3rem !important;
            }


            /* SECONDARY HEADING */
            h2,
            div[data-testid="stHeading"] h2 {
                font-family: 'Outfit', sans-serif !important;
                font-size: 2.2rem !important;
                font-weight: 700 !important;
                line-height: 1.2 !important;
                color: #F7F3EE !important;
                margin-bottom: 0.5rem !important;
            }


            /* SMALLER HEADINGS */
            h3 {
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.6rem !important;
                font-weight: 700 !important;
                color: #F7F3EE !important;
            }

            h4 {
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.2rem !important;
                font-weight: 600 !important;
                color: #F7F3EE !important;
            }


            /* NORMAL TEXT */
            p {
                color: #B8C4D9 !important;
                font-size: 1rem !important;
                font-weight: 400 !important;
                line-height: 1.6 !important;
            }

            

            /* STREAMLIT TEXT */
            .stMarkdown,
            .stMarkdown p,
            .stText {
                color: #B8C4D9 !important;
            }


            /* BUTTONS */
            button[kind="primary"] {
                border-radius: 2.5rem !important;
                background: #4753cc !important;
                color: #FFFFFF !important;
                padding: 10px 20px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                transition: transform 0.25s ease-in-out !important;
            }


            button[kind="secondary"] {
                border-radius: 1.5rem !important;
                background: #4753cc !important;
                color:#FFFFFF  !important;
                padding: 10px 20px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                transition: transform 0.25s ease-in-out !important;
            }


            button:hover {
                transform: scale(1.03) !important;
            }


            .app-header {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 3rem;
            }

            .header-icon {
                font-size: 2.6rem;
            }

            .header-brand {
                font-family: 'Outfit', sans-serif !important;
                font-size: 2.5rem;
                font-weight: 800;
                color: #F7F3EE;
                line-height: 1;
            }

            .header-subtitle {
                font-family: 'Outfit', sans-serif !important;
                font-size: 0.9rem;
                font-weight: 400;
                color: #B8C4D9;
                margin-top: 0.35rem;
            }

            .app-footer {
                text-align: center;
                margin-top: 4rem;
                padding-bottom: 1rem;
                font-family: 'Outfit', sans-serif !important;
                font-size: 0.85rem;
                color: #8FA0B8;
            }


            /* STREAMLIT PAGE SPACING */
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 2rem !important;
            }



            # ---------- SEARCH & FILTER INPUTS ----------

        div[data-testid="stTextInput"] input,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #F1F3F8 !important;
            border: 1px solid #334155 !important;
            border-radius: 10px !important;
        }

        /* Search field */
        div[data-testid="stTextInput"] input {
            color: #1E293B !important;
            box-shadow: 0 0 0 1px rgba(91, 95, 199, 0.15) !important;
        }

        /* Select boxes */
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            color: #1E293B !important;
        }

        /* Focus effect */
        div[data-testid="stTextInput"] input:focus {
            border: 1px solid #5B5FC7 !important;
            box-shadow: 0 0 0 3px rgba(91, 95, 199, 0.18) !important;
        }

        /* Hover effect */
        div[data-testid="stTextInput"] input:hover,
        div[data-testid="stSelectbox"] div[data-baseweb="select"]:hover > div {
            border-color: #5B5FC7 !important;
        }

       /* Fix Streamlit internal icons */
        [data-testid="stIconMaterial"],
        [data-testid="stPopover"] span {
            font-family: "Material Symbols Rounded" !important;
            font-style: normal !important;
            font-weight: normal !important;
            line-height: 1 !important;
        }
        </style>
    """, unsafe_allow_html=True)



