import streamlit as st
import pandas as pd
from src.conexion_sheets import obtener_datos_hoja
from src.calculos_puntaje import calcular_leaderboard


def renderizar_leaderboard(hoja):
    st.subheader("Tabla de posiciones")

    apuestas_raw = obtener_datos_hoja(hoja, "Apuestas")
    resultados_raw = obtener_datos_hoja(hoja, "Resultados")

    if not resultados_raw:
        st.info("Todavía no hay resultados cargados.")
        return

    df_apuestas = pd.DataFrame(apuestas_raw)
    df_resultados = pd.DataFrame(resultados_raw)

    if df_apuestas.empty:
        st.info("No hay apuestas registradas.")
        return

    if not df_resultados.empty:
        df_resultados["Partido"] = (
            df_resultados["Equipo A"] + " vs " + df_resultados["Equipo B"]
        )
        df_resultados = df_resultados.rename(
            columns={"Goles A": "Goles_A_Real", "Goles B": "Goles_B_Real"}
        )

    if not df_apuestas.empty:
        df_apuestas = df_apuestas.rename(columns={"Nombre": "Usuario"})
        df_apuestas["Partido"] = (
            df_apuestas["Equipo A"] + " vs " + df_apuestas["Equipo B"]
        )
        df_apuestas = df_apuestas.rename(
            columns={"Goles A": "Goles_A", "Goles B": "Goles_B"}
        )

    df = calcular_leaderboard(df_apuestas, df_resultados)

    if df.empty:
        st.info("No hay datos suficientes para mostrar.")
        return

    df_estilo = df.style.set_properties(
        **{
            "background-color": "#262730",
            "color": "#FAFAFA",
            "border": "1px solid #555",
            "text-align": "center",
        }
    ).set_table_styles(
        [
            {
                "selector": "th",
                "props": [
                    ("background-color", "#FF4B4B"),
                    ("color", "white"),
                    ("text-align", "center"),
                ],
            },
            {
                "selector": "tr:nth-of-type(1)",
                "props": [("font-weight", "bold"), ("font-size", "1.2em")],
            },
        ]
    )

    st.dataframe(df_estilo, width="stretch", height=400)
