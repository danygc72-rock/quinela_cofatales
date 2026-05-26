import streamlit as st
import pandas as pd
from src.conexion_sheets import obtener_datos_hoja
from src.calculos_puntos import calcular_puntos

MEDALLAS = {1: "🥇", 2: "🥈", 3: "🥉"}


def _renderizar_podio(ranking, usuario_actual):
    if len(ranking) == 0:
        return
    st.subheader("🏆 Podio")
    cols = st.columns(3)
    for i, col in enumerate(cols):
        if i >= len(ranking):
            with col:
                st.write("")
            continue
        fila = ranking.iloc[i]
        pos = i + 1
        nombre = fila["Usuario"]
        puntos = int(fila["Puntos"])
        es_usuario = nombre == usuario_actual
        with col:
            st.markdown(
                f"""
                <div style="text-align: center; padding: 12px;
                    background: {'#1e3a1e' if pos == 1 else '#1e2329'};
                    border-radius: 15px;
                    border: {'2px solid #FFD700' if pos == 1 else '1px solid #333'};
                    {'transform: scale(1.05);' if pos == 1 else ''}
                ">
                    <div style="font-size: 2.5rem;">{MEDALLAS.get(pos, "")}</div>
                    <div style="font-size: 1.5rem; font-weight: 900; color: #00FF41;">
                        {puntos}
                    </div>
                    <div style="font-size: 0.9rem; font-weight: {'700' if es_usuario else '400'};
                         color: {'#FFFFFF' if es_usuario else '#CCC'};
                         margin-top: 4px;">
                        {nombre}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


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
            puntos, exacto = calcular_puntos(goles_a, goles_b, real_a, real_b)
            cruzados.append({
                "Usuario": apuesta["Nombre"],
                "Puntos": puntos,
                "Exacto": 1 if exacto else 0,
            })

    if not cruzados:
        st.info("No hay coincidencias entre apuestas y resultados.")
        return

    df = (
        pd.DataFrame(cruzados)
        .groupby("Usuario")
        .agg(Puntos=("Puntos", "sum"), Exactos=("Exacto", "sum"))
        .reset_index()
        .sort_values(["Puntos", "Exactos"], ascending=[False, False])
        .reset_index(drop=True)
    )
    df.index = df.index + 1
    df.index.name = "Pos"

    if not df.empty and df.iloc[0]["Puntos"] > 0:
        st.balloons()

    _renderizar_podio(df, st.session_state.get("usuario_actual", ""))

    st.markdown("<br>", unsafe_allow_html=True)

    def _estilo_fila(row):
        idx = row.name
        es_leader = idx == 1
        usuario = st.session_state.get("usuario_actual", "")
        es_usuario = row["Usuario"] == usuario
        estilo = []
        if es_leader:
            estilo.append("background-color: rgba(0, 255, 65, 0.12)")
        if es_usuario:
            estilo.append("font-weight: bold")
        return estilo

    df_display = df.copy()
    df_display["Puntos"] = df_display["Puntos"].astype(int)
    df_display["Exactos"] = df_display["Exactos"].astype(int)

    df_estilo = (
        df_display.style
        .apply(_estilo_fila, axis=1)
        .set_properties(
            **{
                "color": "#FAFAFA",
                "border": "1px solid #333",
                "text-align": "center",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#1e2329"),
                        ("color", "#00FF41"),
                        ("text-align", "center"),
                        ("border-bottom", "2px solid #00FF41"),
                    ],
                },
            ]
        )
    )

    st.dataframe(df_estilo, use_container_width=True, height=400)
