import streamlit as st
from src.config import USUARIOS_PERMITIDOS


def renderizar_autenticacion():
    st.subheader("Seleccioná tu nombre")
    usuario = st.selectbox(
        "¿Quién está apostando?",
        options=USUARIOS_PERMITIDOS,
        index=0,
        key="usuario_actual",
    )
    if usuario == USUARIOS_PERMITIDOS[0]:
        st.warning("Seleccioná un nombre para empezar.")
        return None
    return usuario
