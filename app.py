import streamlit as st

st.set_page_config(
    page_title="Quinela Co-fatales 2026",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from src.conexion_sheets import conectar_google_sheets
from src.ui.dashboard import renderizar_countdown_main, renderizar_dashboard
from src.ui.oraculo import renderizar_oraculo
from src.ui.ranking import renderizar_ranking
from src.ui.estilos import aplicar_estilos_modernos


def main():
    aplicar_estilos_modernos()

    hoja = conectar_google_sheets()

    if not hoja:
        st.stop()

    renderizar_countdown_main()

    st.image("assets/logo_mundial.png", width="stretch")

    st.markdown(
        '<h1 class="titulo-mundial" style="margin-top: -10px;">CO-FATALES 2026</h1>',
        unsafe_allow_html=True,
    )
    st.caption("Mundial 2026 — La apuesta de los amigos")

    st.divider()

    pestana = st.selectbox(
        "Navegación",
        options=["Dashboard", "Oráculo IA", "Ranking"],
        key="navegacion",
    )

    st.divider()

    if pestana == "Dashboard":
        renderizar_dashboard(hoja)
    elif pestana == "Oráculo IA":
        renderizar_oraculo()
    elif pestana == "Ranking":
        renderizar_ranking(hoja)

    st.divider()
    st.caption("Hecho con ❤️ para la co-fatales")


if __name__ == "__main__":
    main()
