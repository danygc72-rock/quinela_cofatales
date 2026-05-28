from datetime import datetime, timezone

import streamlit as st

from src.conexion_sheets import (
    agregar_fila,
    obtener_partidos_activos,
    obtener_proximos_partidos,
)
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


def renderizar_countdown_main():
    inicio_mundial = datetime(2026, 6, 11, tzinfo=timezone.utc)
    ahora = datetime.now(timezone.utc)
    if ahora >= inicio_mundial:
        st.markdown(
            """
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1e2329, #151a20);
                 border-radius: 16px; border: 1px solid #D4AF37; margin-bottom: 20px;">
                <span style="font-size: 2.5rem;">🏆</span>
                <div style="color: #D4AF37; font-weight: 800; font-size: 1.3rem; margin-top: 6px;">
                    ¡Mundial 2026 en marcha!
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return
    dias = (inicio_mundial - ahora).days
    horas = int((inicio_mundial - ahora).seconds / 3600)
    total_dias = (inicio_mundial - datetime(2025, 1, 1, tzinfo=timezone.utc)).days
    pct = max(0, min(100, (1 - dias / total_dias) * 100))
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1e2329 0%, #151a20 100%);
             border-radius: 16px; padding: 20px; margin-bottom: 20px;
             border: 1px solid #2a2a2a; box-shadow: 0 4px 24px rgba(0,0,0,0.4);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div style="flex: 1; min-width: 120px;">
                    <div style="font-size: 0.65rem; color: #888; letter-spacing: 2px;
                         text-transform: uppercase; margin-bottom: 4px;">
                        Cuenta regresiva
                    </div>
                    <div style="font-size: 0.85rem; color: #D4AF37; font-weight: 600;
                         letter-spacing: 1px;">
                        Mundial 2026
                    </div>
                </div>
                <div style="display: flex; gap: 16px;">
                    <div style="text-align: center;">
                        <div style="font-size: 2.2rem; font-weight: 900; color: #D4AF37;
                             line-height: 1.1; text-shadow: 0 0 16px rgba(212, 175, 55, 0.3);">
                            {dias}
                        </div>
                        <div style="font-size: 0.6rem; color: #666; letter-spacing: 2px;">
                            DÍAS
                        </div>
                    </div>
                    <div style="font-size: 2rem; color: #333; font-weight: 100; line-height: 1.8;">:</div>
                    <div style="text-align: center;">
                        <div style="font-size: 2.2rem; font-weight: 900; color: #D4AF37;
                             line-height: 1.1; text-shadow: 0 0 16px rgba(212, 175, 55, 0.3);">
                            {horas}
                        </div>
                        <div style="font-size: 0.6rem; color: #666; letter-spacing: 2px;">
                            HORAS
                        </div>
                    </div>
                </div>
            </div>
            <div style="margin-top: 14px; background: #0e1117; border-radius: 20px;
                 height: 6px; overflow: hidden; border: 1px solid #2a2a2a;">
                <div style="width: {pct:.1f}%; height: 100%;
                     background: linear-gradient(90deg, #D4AF37, #FFD700);
                     border-radius: 20px;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 6px;
                 font-size: 0.6rem; color: #555;">
                <span>Inicio</span>
                <span>{pct:.0f}%</span>
                <span>11 Jun 2026</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def renderizar_dashboard(hoja):
    st.caption("🏟️ Los horarios están en UTC. Las apuestas se cierran al inicio oficial del partido.")

    proximos = obtener_proximos_partidos()
    if proximos:
        st.markdown(
            '<div style="text-align: center; margin-bottom: 10px;">'
            '<span style="color: #D4AF37; font-weight: 700; font-size: 0.9rem; letter-spacing: 1px;">📅 PRÓXIMOS PARTIDOS</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        fecha_actual = None
        for p in proximos:
            if p["fecha_utc"] != fecha_actual:
                fecha_actual = p["fecha_utc"]
                st.markdown(
                    f"""
                    <div style="font-size: 0.75rem; color: #888; letter-spacing: 1px;
                         margin: 8px 0 4px 0; text-align: center;">
                        ── {p['fecha_legible'].upper()} ──
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            cols = st.columns([1, 4])
            with cols[0]:
                st.markdown(
                    f'<div style="font-size: 1.2rem; text-align: center; padding-top: 8px;">{_bandera(p["Equipo_A"])} vs {_bandera(p["Equipo_B"])}</div>',
                    unsafe_allow_html=True,
                )
            with cols[1]:
                st.markdown(
                    f"""
                    <div style="background: #1a1f26; border-radius: 10px; padding: 8px 14px;
                         border: 1px solid #2a2a2a; margin: 3px 0;
                         display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.85rem; font-weight: 600; color: #FAFAFA;">
                            {p['Equipo_A']} vs {p['Equipo_B']}
                        </span>
                        <span style="font-size: 0.75rem; color: #D4AF37; letter-spacing: 1px;">
                            🕐 {p['hora_utc']} UTC
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.divider()

    usuario = st.session_state.get("usuario_nombre", "")
    if not usuario:
        st.warning("No se encontró usuario autenticado.")
        return

    partidos = obtener_partidos_activos()

    if not partidos:
        partidos = proximos or []
        if partidos:
            st.info("📋 No hay partidos para hoy. Puedes pronosticar los **próximos partidos** con anticipación.")
        else:
            st.info("⚽ No hay partidos disponibles para pronósticos en este momento. ¡Atento a la próxima jornada!")
            return

    es_futuro = not obtener_partidos_activos()

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
                    <div style="color: #D4AF37; font-weight: 700; font-size: 1.1rem;">
                        🕐 {hora} UTC
                    </div>
                </div>
                <div style="color: #888; font-size: 0.85rem; margin-top: 6px;">
                    {'🗓️ Pronóstico anticipado' if es_futuro else '🏟️ Estadio Mundial 2026'}
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
                    ranking = calcular_tabla(hoja)
                    prediccion = obtener_prediccion_oraculo(todos, ranking)
                    st.success(prediccion)
                except (ConnectionError, RuntimeError) as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Error inesperado: {e}")
