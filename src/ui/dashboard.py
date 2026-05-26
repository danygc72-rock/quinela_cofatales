from datetime import datetime
import streamlit as st
from src.config import PARTIDOS_FIXTURE
from src.conexion_sheets import agregar_fila
from src.services.ai_service import obtener_prediccion


def _partido_cerrado(limite_str):
    if not limite_str:
        return False
    try:
        limite = datetime.strptime(limite_str, "%Y-%m-%d %H:%M:%S")
        return datetime.now() > limite
    except ValueError:
        return False


def renderizar_dashboard(hoja, usuario):
    st.subheader(f"Pronosticá el partido de hoy, {usuario}")

    opciones = [
        p["partido"] + (f" — Cierra: {p['limite']}" if p["limite"] else "")
        for p in PARTIDOS_FIXTURE
    ]

    seleccion = st.selectbox(
        "Seleccioná un partido",
        options=opciones,
        index=0,
        key="partido_seleccionado",
    )

    partido_actual = None
    for p in PARTIDOS_FIXTURE:
        if p["partido"] in seleccion:
            partido_actual = p
            break

    if not partido_actual or partido_actual["partido"] == PARTIDOS_FIXTURE[0]["partido"]:
        st.info("Elegí un partido para pronosticar.")
        return

    cerrado = _partido_cerrado(partido_actual["limite"])

    equipos = partido_actual["partido"].split(" vs ")
    equipo_a = equipos[0].strip()
    equipo_b = equipos[1].split(" (")[0].strip() if "(" in equipos[1] else equipos[1].strip()

    if cerrado:
        st.warning("El partido ya comenzó. Apuestas cerradas.")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Local", equipo_a)
        goles_a = st.number_input("Goles", min_value=0, max_value=20, step=1, key="gol_a", disabled=cerrado)
    with col2:
        st.metric("Visitante", equipo_b)
        goles_b = st.number_input("Goles", min_value=0, max_value=20, step=1, key="gol_b", disabled=cerrado)

    if st.button("Enviar apuesta", type="primary", use_container_width=True, disabled=cerrado):
        datos = [usuario, equipo_a.upper(), equipo_b.upper(), goles_a, goles_b]
        if agregar_fila(hoja, datos):
            st.success("Apuesta registrada correctamente!")
            st.balloons()
        else:
            st.error("No se pudo guardar la apuesta.")

    st.divider()
    with st.expander("Preguntarle a la IA"):
        if st.button("El Oráculo", type="secondary", use_container_width=True):
            with st.spinner("El Oráculo está consultando los astros..."):
                try:
                    prediccion = obtener_prediccion(partido_actual["partido"])
                    st.success(prediccion)
                except (ConnectionError, RuntimeError) as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Error inesperado: {e}")
