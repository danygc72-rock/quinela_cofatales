import streamlit as st

from src.conexion_sheets import obtener_usuarios


def renderizar_autenticacion():
    df_usuarios = obtener_usuarios()
    if df_usuarios.empty:
        st.error("No se pudo cargar la lista de usuarios.")
        return None

    opciones = [
        f"{row['Nombre']} {row['Bandera']}"
        for _, row in df_usuarios.iterrows()
    ]
    opciones.insert(0, "Selecciona tu nombre...")

    st.subheader("Seleccioná tu nombre")
    seleccion = st.selectbox(
        "¿Quién está apostando?",
        options=opciones,
        index=0,
        key="usuario_actual",
    )

    if seleccion == opciones[0]:
        st.warning("Seleccioná un nombre para empezar.")
        return None

    nombre_limpio = seleccion.rsplit(" ", 1)[0]
    return nombre_limpio
