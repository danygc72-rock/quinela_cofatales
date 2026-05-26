import streamlit as st
import pandas as pd
from src.conexion_sheets import obtener_datos_hoja
from src.calculos_puntos import calcular_puntos


def renderizar_ranking(hoja):
    st.subheader("Tabla de posiciones")

    apuestas_raw = obtener_datos_hoja(hoja, "Apuestas")
    fixture_raw = obtener_datos_hoja(hoja, "Fixture")

    if not apuestas_raw:
        st.info("No hay apuestas registradas.")
        return

    if not fixture_raw:
        st.info("No hay datos del fixture.")
        return

    df_apuestas = pd.DataFrame(apuestas_raw)
    df_fixture = pd.DataFrame(fixture_raw)

    df_fixture = df_fixture[df_fixture["Estado"] == "Terminado"].copy()

    if df_fixture.empty:
        st.info("Todavía no hay partidos terminados. Los puntajes se calcularán automáticamente cuando finalicen.")
        return

    cruzados = []
    for _, apuesta in df_apuestas.iterrows():
        equipo_a = apuesta["Equipo A"]
        equipo_b = apuesta["Equipo B"]
        goles_a = apuesta["Goles A"]
        goles_b = apuesta["Goles B"]

        match = df_fixture[
            (df_fixture["Equipo_A"] == equipo_a)
            & (df_fixture["Equipo_B"] == equipo_b)
        ]

        if match.empty:
            continue

        for _, partido in match.iterrows():
            real_a = partido["Goles_A_Real"]
            real_b = partido["Goles_B_Real"]
            puntos = calcular_puntos(goles_a, goles_b, real_a, real_b)
            cruzados.append({
                "Usuario": apuesta["Nombre"],
                "Puntos": puntos,
            })

    if not cruzados:
        st.info("No hay coincidencias entre apuestas y resultados.")
        return

    df_puntos = (
        pd.DataFrame(cruzados)
        .groupby("Usuario")["Puntos"]
        .sum()
        .reset_index()
        .sort_values("Puntos", ascending=False)
        .reset_index(drop=True)
    )
    df_puntos.index = df_puntos.index + 1
    df_puntos.index.name = "Pos"

    if not df_puntos.empty and df_puntos.iloc[0]["Puntos"] > 0:
        st.balloons()

    df_estilo = df_puntos.style.set_properties(
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

    st.dataframe(df_estilo, use_container_width=True, height=400)
