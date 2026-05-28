import streamlit as st


def aplicar_estilos_modernos():
    st.markdown(
        """
        <style>
        .match-card {
            border-radius: 15px;
            border-left: 5px solid #D4AF37;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            padding: 20px;
            margin: 10px 0;
            background-color: #1e2329;
            transition: all 0.3s ease;
        }
        .match-card:hover {
            transform: translateY(-4px);
            border-left-color: #FFD700;
            box-shadow: 0 8px 24px rgba(212, 175, 55, 0.3);
        }
        .titulo-mundial {
            background: linear-gradient(135deg, #D4AF37 0%, #FFD700 50%, #D4AF37 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            font-size: 2.5rem;
        }
        div.stButton > button {
            background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
            color: #0e1117 !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            border: none !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            transform: scale(1.03);
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
        }
        div.stButton > button[kind="secondary"] {
            background: #1a1f26 !important;
            color: #CCC !important;
            border: 1px solid #333 !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            border-color: #D4AF37 !important;
            color: #FAFAFA !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
