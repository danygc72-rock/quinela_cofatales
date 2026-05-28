import streamlit as st
import pandas as pd
from src.conexion_sheets import obtener_datos_hoja, obtener_usuarios
from src.calculos_puntos import calcular_puntos

MEDALLAS = {1: "🥇", 2: "🥈", 3: "🥉"}


def _cargar_banderas():
    df = obtener_usuarios()
    if df.empty:
        return {}
    return dict(zip(df["Nombre"], df["Bandera"]))


def _renderizar_podio(ranking, usuario_actual, banderas):
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
        bandera = banderas.get(nombre, "")
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
                    <div style="font-size: 1.5rem; font-weight: 900; color: #D4AF37;">
                        {puntos}
                    </div>
                    <div style="font-size: 1.3rem; margin-top: 2px;">
                        {bandera}
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
    banderas = _cargar_banderas()

    if df_fixture.empty:
        st.info("⏳ Sin partidos finalizados aún — la tabla se actualizará automáticamente cuando haya resultados.")
        df_usuarios = obtener_usuarios()
        if df_usuarios.empty:
            return
        df = pd.DataFrame({
            "Usuario": df_usuarios["Nombre"].sort_values(),
            "Puntos": 0,
            "Exactos": 0,
        }).reset_index(drop=True)
        mostrar_podio = False
    else:
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
        mostrar_podio = True
    df.index = df.index + 1
    df.index.name = "Pos"

    if mostrar_podio and not df.empty and df.iloc[0]["Puntos"] > 0:
        st.balloons()
        _renderizar_podio(df, st.session_state.get("usuario_nombre", ""), banderas)

    st.markdown("<br>", unsafe_allow_html=True)

    def _estilo_fila(row):
        idx = row.name
        es_leader = mostrar_podio and idx == 1
        usuario_sesion = st.session_state.get("usuario_nombre", "")
        es_usuario = row["Usuario"] == usuario_sesion
        css = ""
        if es_leader:
            css += "background-color: rgba(212, 175, 55, 0.12);"
        if es_usuario:
            css += "font-weight: bold;"
        return [css] * len(row)

    df_display = df.copy()
    df_display.insert(0, "", df_display["Usuario"].map(banderas).fillna(""))
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
                        ("color", "#D4AF37"),
                        ("text-align", "center"),
                        ("border-bottom", "2px solid #D4AF37"),
                    ],
                },
            ]
        )
    )

    st.dataframe(df_estilo, width="stretch", height=400)
