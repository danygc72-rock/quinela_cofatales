from datetime import datetime, timezone

import streamlit as st

from src.conexion_sheets import agregar_fila, obtener_partidos_activos
from src.services.ai_service import obtener_prediccion

BANDERAS = {
    "Algeria": "🇩🇿", "Argentina": "🇦🇷", "Australia": "🇦🇺", "Austria": "🇦🇹",
    "Belgium": "🇧🇪", "Bosnia-Herzegovina": "🇧🇦", "Brazil": "🇧🇷",
    "Canada": "🇨🇦", "Cape Verde Islands": "🇨🇻", "Colombia": "🇨🇴",
    "Congo DR": "🇨🇩", "Croatia": "🇭🇷", "Curaçao": "🇨🇼", "Czechia": "🇨🇿",
    "Ecuador": "🇪🇨", "Egypt": "🇪🇬", "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "France": "🇫🇷", "Germany": "🇩🇪", "Ghana": "🇬🇭", "Haiti": "🇭🇹",
    "Iran": "🇮🇷", "Iraq": "🇮🇶", "Ivory Coast": "🇨🇮",
    "Japan": "🇯🇵", "Jordan": "🇯🇴", "Mexico": "🇲🇽", "Morocco": "🇲🇦",
    "Netherlands": "🇳🇱", "New Zealand": "🇳🇿", "Norway": "🇳🇴",
    "Panama": "🇵🇦", "Paraguay": "🇵🇾", "Portugal": "🇵🇹",
    "Qatar": "🇶🇦", "Saudi Arabia": "🇸🇦", "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Senegal": "🇸🇳", "South Africa": "🇿🇦", "South Korea": "🇰🇷",
    "Spain": "🇪🇸", "Sweden": "🇸🇪", "Switzerland": "🇨🇭",
    "Tunisia": "🇹🇳", "Turkey": "🇹🇷", "United States": "🇺🇸",
    "Uruguay": "🇺🇾", "Uzbekistan": "🇺🇿",
}


def _bandera(pais):
    return BANDERAS.get(pais, "🏳️")


def _renderizar_countdown():
    inicio_mundial = datetime(2026, 6, 11, tzinfo=timezone.utc)
    ahora = datetime.now(timezone.utc)
    if ahora >= inicio_mundial:
        st.sidebar.metric("Mundial 2026", "¡En marcha!")
        return
    dias = (inicio_mundial - ahora).days
    horas = int((inicio_mundial - ahora).seconds / 3600)
    st.sidebar.metric("Cuenta regresiva", f"{dias} días")
    st.sidebar.caption(f"{horas}h hasta el primer partido")


def renderizar_dashboard(hoja, usuario):
    _renderizar_countdown()

    st.markdown(
        '<h1 class="titulo-mundial">CO-FATALES 2026</h1>',
        unsafe_allow_html=True,
    )
    st.caption("Los horarios están en UTC. Las apuestas se cierran al inicio oficial del partido.")

    partidos = obtener_partidos_activos()

    if not partidos:
        st.info("⚽ No hay partidos abiertos para pronósticos en este momento. ¡Atento a la próxima jornada!")
        return

    for partido in partidos:
        eq_a = partido["Equipo_A"]
        eq_b = partido["Equipo_B"]
        hora = partido.get("hora_utc", "--:--")

        st.markdown(
            f"""
            <div class="match-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 1.8rem;">
                        {_bandera(eq_a)} {eq_a}
                        <span style="color: #FFD700; margin: 0 12px;">vs</span>
                        {eq_b} {_bandera(eq_b)}
                    </div>
                    <div style="color: #00FF41; font-weight: 700; font-size: 1.1rem;">
                        🕐 {hora} UTC
                    </div>
                </div>
                <div style="color: #888; font-size: 0.85rem; margin-top: 6px;">
                    🏟️ Estadio Mundial 2026
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_a, col_b, col_btn = st.columns([1, 1, 2])
        with col_a:
            goles_a = st.number_input(
                f"{eq_a}", min_value=0, max_value=20, step=1,
                key=f"gol_a_{partido['ID']}",
            )
        with col_b:
            goles_b = st.number_input(
                f"{eq_b}", min_value=0, max_value=20, step=1,
                key=f"gol_b_{partido['ID']}",
            )
        with col_btn:
            st.write("")
            st.write("")
            if st.button(
                "Guardar Pronóstico",
                type="primary",
                use_container_width=True,
                key=f"btn_{partido['ID']}",
            ):
                datos = [usuario, eq_a.upper(), eq_b.upper(), goles_a, goles_b]
                if agregar_fila(hoja, datos):
                    st.success("Apuesta registrada correctamente!")
                    st.balloons()
                else:
                    st.error("No se pudo guardar la apuesta.")

    st.divider()
    with st.expander("Preguntarle a la IA"):
        todos = " - ".join(
            f"{p['Equipo_A']} vs {p['Equipo_B']}"
            for p in partidos
        )
        if st.button("El Oráculo", type="secondary", use_container_width=True):
            with st.spinner("El Oráculo está consultando los astros..."):
                try:
                    prediccion = obtener_prediccion(todos)
                    st.success(prediccion)
                except (ConnectionError, RuntimeError) as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Error inesperado: {e}")
