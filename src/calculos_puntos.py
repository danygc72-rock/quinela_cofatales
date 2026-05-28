import pandas as pd


def _signo(goles_a, goles_b):
    if goles_a > goles_b:
        return "local"
    if goles_b > goles_a:
        return "visita"
    return "empate"


def calcular_puntos(apuesta_a, apuesta_b, real_a, real_b):
    if apuesta_a == real_a and apuesta_b == real_b:
        return 5, True

    mismo_signo = _signo(apuesta_a, apuesta_b) == _signo(real_a, real_b)
    un_gol_acertado = (apuesta_a == real_a) or (apuesta_b == real_b)

    if mismo_signo and un_gol_acertado:
        return 3, False
    if mismo_signo:
        return 2, False
    if un_gol_acertado:
        return 1, False
    return 0, False


def calcular_tabla(hoja):
    from src.conexion_sheets import obtener_datos_hoja

    apuestas_raw = obtener_datos_hoja(hoja, "Apuestas")
    fixture_raw = obtener_datos_hoja(hoja, "Fixture")

    if not apuestas_raw or not fixture_raw:
        return None

    df_apuestas = pd.DataFrame(apuestas_raw)
    df_fixture = pd.DataFrame(fixture_raw)
    df_fixture = df_fixture[df_fixture["Estado"] == "Terminado"]

    if df_fixture.empty:
        return None

    cruzados = []
    for _, apuesta in df_apuestas.iterrows():
        match = df_fixture[
            (df_fixture["Equipo_A"] == apuesta["Equipo A"])
            & (df_fixture["Equipo_B"] == apuesta["Equipo B"])
        ]
        for _, partido in match.iterrows():
            puntos, exacto = calcular_puntos(
                apuesta["Goles A"], apuesta["Goles B"],
                partido["Goles_A_Real"], partido["Goles_B_Real"],
            )
            cruzados.append({
                "Usuario": apuesta["Nombre"],
                "Puntos": puntos,
                "Exacto": 1 if exacto else 0,
            })

    if not cruzados:
        return None

    return (
        pd.DataFrame(cruzados)
        .groupby("Usuario")
        .agg(Puntos=("Puntos", "sum"), Exactos=("Exacto", "sum"))
        .reset_index()
        .sort_values(["Puntos", "Exactos"], ascending=[False, False])
        .reset_index(drop=True)
    )
