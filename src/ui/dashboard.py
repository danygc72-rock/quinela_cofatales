from datetime import datetime, timezone

import streamlit as st

from src.conexion_sheets import (
    agregar_fila,
    obtener_partidos_activos,
    obtener_proximos_partidos,
    obtener_usuarios,
)
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
    st.sidebar.markdown(
        """
        <div style="text-align: center; margin: 10px 0;">
            <span style="font-size: 2.5rem;">⚽</span>
            <div style="font-size: 0.85rem; color: #D4AF37; font-weight: 700; letter-spacing: 2px; text-shadow: 0 0 8px rgba(212, 175, 55, 0.3);">
                WORLD CUP 2026
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.divider()
    inicio_mundial = datetime(2026, 6, 11, tzinfo=timezone.utc)
    ahora = datetime.now(timezone.utc)
    if ahora >= inicio_mundial:
        st.sidebar.markdown(
            """
            <div style="text-align: center; padding: 12px; background: #1e2329;
                 border-radius: 12px; border: 1px solid #D4AF37;">
                <span style="font-size: 1.8rem;">🏆</span>
                <div style="color: #D4AF37; font-weight: 800; font-size: 1.1rem;">
                    ¡Mundial en marcha!
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
    st.sidebar.markdown(
        f"""
        <div style="text-align: center; padding: 16px 12px; background: #1e2329;
             border-radius: 14px; border: 1px solid #333;
             box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
            <div style="font-size: 0.7rem; color: #888; letter-spacing: 2px;
                 text-transform: uppercase; margin-bottom: 8px;">
                Cuenta regresiva
            </div>
            <div style="display: flex; justify-content: center; gap: 12px;">
                <div style="background: #0e1117; border-radius: 10px; padding: 8px 14px;
                     min-width: 60px; border: 1px solid #2a2a2a;">
                    <div style="font-size: 1.8rem; font-weight: 900; color: #D4AF37;
                         line-height: 1.2; text-shadow: 0 0 12px rgba(212, 175, 55, 0.3);">
                        {dias}
                    </div>
                    <div style="font-size: 0.6rem; color: #888; letter-spacing: 1px;">
                        DÍAS
                    </div>
                </div>
                <div style="background: #0e1117; border-radius: 10px; padding: 8px 14px;
                     min-width: 60px; border: 1px solid #2a2a2a;">
                    <div style="font-size: 1.8rem; font-weight: 900; color: #D4AF37;
                         line-height: 1.2; text-shadow: 0 0 12px rgba(212, 175, 55, 0.3);">
                        {horas}
                    </div>
                    <div style="font-size: 0.6rem; color: #888; letter-spacing: 1px;">
                        HORAS
                    </div>
                </div>
            </div>
            <div style="margin-top: 12px; background: #0e1117; border-radius: 20px;
                 height: 6px; overflow: hidden; border: 1px solid #2a2a2a;">
                <div style="width: {pct:.1f}%; height: 100%;
                     background: linear-gradient(90deg, #D4AF37, #FFD700);
                     border-radius: 20px; transition: width 0.5s;"></div>
            </div>
            <div style="font-size: 0.65rem; color: #666; margin-top: 6px;">
                {pct:.0f}% del camino
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _seleccionar_usuario():
    df_usuarios = obtener_usuarios()
    if df_usuarios.empty:
        st.error("No se pudo cargar la lista de usuarios.")
        return None

    df_usuarios = df_usuarios.sort_values("Nombre").reset_index(drop=True)
    opciones = [
        f"{row['Nombre']} {row['Bandera']}"
        for _, row in df_usuarios.iterrows()
    ]
    placeholder = "Selecciona tu nombre..."
    opciones.insert(0, placeholder)

    seleccion = st.selectbox(
        "¿Quién está apostando?",
        options=opciones,
        index=0,
        key="usuario_actual",
    )

    if seleccion == placeholder:
        st.warning("Seleccioná tu nombre para empezar.")
        return None

    nombre_limpio = seleccion.rsplit(" ", 1)[0]
    st.session_state.usuario_nombre = nombre_limpio
    return nombre_limpio


def _pin_correcto(usuario):
    df_usuarios = obtener_usuarios()
    if df_usuarios.empty:
        return False
    match = df_usuarios[df_usuarios["Nombre"] == usuario]
    if match.empty:
        return False
    pin_real = str(match.iloc[0]["PIN"]).strip()
    pin_ingresado = st.text_input(
        "🔐 PIN de Acceso",
        type="password",
        key="pin_dashboard",
        placeholder="Ingresá tu PIN de 4 dígitos",
    )
    if not pin_ingresado:
        return False
    return pin_ingresado.strip() == pin_real


def renderizar_dashboard(hoja):
    _renderizar_countdown()

    st.caption("🏟️ Los horarios están en UTC. Las apuestas se cierran al inicio oficial del partido.")

    proximos = obtener_proximos_partidos()
    if proximos:
        with st.expander("📅 Próximos partidos", expanded=False):
            fecha_actual = None
            for p in proximos:
                if p["fecha_utc"] != fecha_actual:
                    fecha_actual = p["fecha_utc"]
                    st.markdown(f"**── {p['fecha_legible']} ──**")
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between;
                         align-items: center; padding: 6px 12px;
                         background: #1a1f26; border-radius: 8px; margin: 4px 0;">
                        <span style="font-size: 1.1rem;">
                            {_bandera(p['Equipo_A'])} {p['Equipo_A']}
                            <span style="color: #FFD700; margin: 0 8px;">vs</span>
                            {p['Equipo_B']} {_bandera(p['Equipo_B'])}
                        </span>
                        <span style="color: #D4AF37; font-size: 0.85rem;">
                            🕐 {p['hora_utc']} UTC
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    usuario = _seleccionar_usuario()
    if not usuario:
        return

    if not _pin_correcto(usuario):
        st.warning("PIN incorrecto. Ingresá el PIN correcto para hacer apuestas.")
        return

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
                    <div style="color: #D4AF37; font-weight: 700; font-size: 1.1rem;">
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
