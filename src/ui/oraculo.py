import streamlit as st
from src.services.ai_service import obtener_prediccion


def renderizar_oraculo():
    st.subheader("El Oráculo IA")

    partido = st.text_input(
        "Escribí el partido (ej: Argentina vs Brasil)",
        key="oraculo_partido",
    )

    if st.button("Consultar al Oráculo", type="primary", use_container_width=True):
        if not partido:
            st.error("Completá el partido.")
            return
        with st.spinner("El Oráculo está consultando los astros..."):
            try:
                prediccion = obtener_prediccion(partido)
                st.success(prediccion)
            except (ConnectionError, RuntimeError) as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error inesperado: {e}")
