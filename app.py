import streamlit as st

st.set_page_config(
    page_title="Quinela Co-fatales 2026",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from src.conexion_sheets import conectar_google_sheets
from src.ui.auth import login, renderizar_ticket, renderizar_sidebar_usuario
from src.ui.dashboard import renderizar_countdown_main, renderizar_dashboard
from src.ui.oraculo import renderizar_oraculo
from src.ui.ranking import renderizar_ranking
from src.ui.estilos import aplicar_estilos_modernos


def main():
    aplicar_estilos_modernos()

    hoja = conectar_google_sheets()
    if not hoja:
        st.stop()

    if not st.session_state.get("autenticado"):
        login(hoja)
        return

    if st.session_state.get("mostrar_ticket"):
        renderizar_ticket()
        return

    renderizar_sidebar_usuario()

    renderizar_countdown_main()

    st.image("assets/logo_mundial.png", width="stretch")

    st.markdown(
        '<h1 class="titulo-mundial" style="margin-top: -10px;">CO-FATALES 2026</h1>',
        unsafe_allow_html=True,
    )
    st.caption("Mundial 2026 — La apuesta de los amigos")

    pestana = st.session_state.get("navegacion", "Dashboard")

    col1, col2, col3 = st.columns(3)
    with col1:
        activo = pestana == "Dashboard"
        if st.button("📊 Dashboard", use_container_width=True,
                     type="primary" if activo else "secondary",
                     key="nav_dashboard"):
            st.session_state.navegacion = "Dashboard"
            st.rerun()
    with col2:
        activo = pestana == "Oráculo IA"
        if st.button("🔮 Oráculo IA", use_container_width=True,
                     type="primary" if activo else "secondary",
                     key="nav_oraculo"):
            st.session_state.navegacion = "Oráculo IA"
            st.rerun()
    with col3:
        activo = pestana == "Ranking"
        if st.button("🏆 Ranking", use_container_width=True,
                     type="primary" if activo else "secondary",
                     key="nav_ranking"):
            st.session_state.navegacion = "Ranking"
            st.rerun()

    st.divider()

    if pestana == "Dashboard":
        renderizar_dashboard(hoja)
    elif pestana == "Oráculo IA":
        renderizar_oraculo(hoja)
    elif pestana == "Ranking":
        renderizar_ranking(hoja)

    st.divider()
    st.caption("Hecho con ❤️ para la co-fatales")


if __name__ == "__main__":
    main()
