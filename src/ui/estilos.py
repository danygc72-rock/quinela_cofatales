import streamlit as st


def aplicar_estilos_modernos():
    st.markdown(
        """
        <style>
        .match-card {
            border-radius: 15px;
            border-left: 5px solid #00FF41;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            padding: 20px;
            margin: 10px 0;
            background-color: #1e2329;
            transition: all 0.3s ease;
        }
        .match-card:hover {
            transform: translateY(-4px);
            border-left-color: #FFD700;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
        }
        .titulo-mundial {
            background: linear-gradient(135deg, #00FF41 0%, #FFD700 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            font-size: 2.5rem;
        }
        div.stButton > button {
            background: linear-gradient(135deg, #00FF41 0%, #00cc33 100%) !important;
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
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.4);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
