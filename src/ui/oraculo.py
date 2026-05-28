import streamlit as st
from src.conexion_sheets import obtener_proximos_partidos
from src.calculos_puntos import calcular_tabla
from src.oraculo_ia import obtener_prediccion_oraculo

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


def renderizar_oraculo(hoja):
    st.subheader("🔮 El Oráculo de los Co-fatales")

    partidos = obtener_proximos_partidos()

    if not partidos:
        st.info("No hay partidos próximos para consultar.")
        return

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
        with st.spinner("El Oráculo está consultando los astros..."):
            try:
                ranking = calcular_tabla(hoja)
                prediccion = obtener_prediccion_oraculo(todos, ranking)
                st.markdown(
                    f"""
                    <div style="background: #1a1f26; border: 1px solid #D4AF37;
                         border-radius: 12px; padding: 20px; margin: 12px 0;
                         box-shadow: 0 0 20px rgba(212, 175, 55, 0.15);
                         color: #FAFAFA; font-size: 0.95rem; line-height: 1.7;
                         white-space: pre-wrap;">
                        {prediccion}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except (ConnectionError, RuntimeError) as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error inesperado: {e}")
