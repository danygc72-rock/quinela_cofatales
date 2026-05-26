import streamlit as st
from src.conexion_sheets import obtener_proximos_partidos
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


def renderizar_oraculo():
    st.subheader("🔮 El Oráculo IA")

    partidos = obtener_proximos_partidos()

    if not partidos:
        st.info("No hay partidos próximos para consultar.")
        todos = ""
    else:
        st.markdown(
            "📅 **Partidos de la próxima jornada**",
            help="El Oráculo analizará estos partidos",
        )
        for p in partidos:
            st.markdown(
                f"""
                <div style="background: #1a1f26; border-radius: 10px; padding: 10px 14px;
                     margin: 4px 0; border: 1px solid #2a2a2a;
                     display: flex; justify-content: space-between; align-items: center;">
                    <span>
                        {_bandera(p['Equipo_A'])} {p['Equipo_A']}
                        <span style="color: #D4AF37; margin: 0 8px;">vs</span>
                        {p['Equipo_B']} {_bandera(p['Equipo_B'])}
                    </span>
                    <span style="color: #888; font-size: 0.8rem;">
                        {p['fecha_legible']} 🕐 {p['hora_utc']} UTC
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        todos = " - ".join(
            f"{p['Equipo_A']} vs {p['Equipo_B']}"
            for p in partidos
        )

    st.divider()

    if st.button("🔮 Consultar al Oráculo", type="primary", use_container_width=True):
        if not todos:
            st.error("No hay partidos para consultar.")
            return
        with st.spinner("El Oráculo está consultando los astros..."):
            try:
                prediccion = obtener_prediccion(todos)
                st.success(prediccion)
            except (ConnectionError, RuntimeError) as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error inesperado: {e}")
