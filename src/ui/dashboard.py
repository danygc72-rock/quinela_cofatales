import streamlit as st
from src.conexion_sheets import agregar_fila, obtener_partidos_activos
from src.services.ai_service import obtener_prediccion


def renderizar_dashboard(hoja, usuario):
    st.subheader(f"Pronosticá el partido de hoy, {usuario}")

    partidos = obtener_partidos_activos()

    if not partidos:
        st.info("⚽ No hay partidos abiertos para pronósticos en este momento. ¡Atento a la próxima jornada!")
        return

    opciones = ["Selecciona un partido..."] + partidos

    seleccion = st.selectbox(
        "Seleccioná un partido",
        options=opciones,
        index=0,
        key="partido_seleccionado",
    )

    st.caption("Los horarios están en UTC. Las apuestas se cierran al inicio oficial del partido.")

    if seleccion == opciones[0]:
        st.info("Elegí un partido para pronosticar.")
        return

    equipos = seleccion.split(" vs ")
    equipo_a = equipos[0].strip()
    equipo_b = equipos[1].strip()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Local", equipo_a)
        goles_a = st.number_input("Goles", min_value=0, max_value=20, step=1, key="gol_a")
    with col2:
        st.metric("Visitante", equipo_b)
        goles_b = st.number_input("Goles", min_value=0, max_value=20, step=1, key="gol_b")

    if st.button("Enviar apuesta", type="primary", use_container_width=True):
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
                    prediccion = obtener_prediccion(seleccion)
                    st.success(prediccion)
                except (ConnectionError, RuntimeError) as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Error inesperado: {e}")
