import streamlit as st

st.set_page_config(
    page_title="Quinela Co-fatales 2026",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from src.conexion_sheets import conectar_google_sheets
from src.ui.auth import renderizar_autenticacion
from src.ui.dashboard import renderizar_dashboard
from src.ui.oraculo import renderizar_oraculo
from src.ui.ranking import renderizar_ranking
from src.ui.estilos import aplicar_estilos_modernos


def main():
    aplicar_estilos_modernos()
    st.title("⚽ Quinela Co-fatales 2026")
    st.caption("Mundial 2026 — La apuesta de los amigos")

    hoja = conectar_google_sheets()

    if not hoja:
        st.stop()

    st.divider()

    usuario = renderizar_autenticacion()
    if not usuario:
        st.stop()

    pestana = st.selectbox(
        "Navegación",
        options=["Dashboard", "Oráculo IA", "Ranking"],
        key="navegacion",
    )

    st.divider()

    if pestana == "Dashboard":
        renderizar_dashboard(hoja, usuario)
    elif pestana == "Oráculo IA":
        renderizar_oraculo()
    elif pestana == "Ranking":
        renderizar_ranking(hoja)

    st.divider()
    st.caption("Hecho con ❤️ para la co-fatales")


if __name__ == "__main__":
    main()
