import pandas as pd
import numpy as np


def calcular_leaderboard(df_apuestas, df_resultados):
    if df_apuestas.empty and df_resultados.empty:
        return pd.DataFrame(columns=["Usuario", "Puntos"])
    if df_apuestas.empty or df_resultados.empty:
        return pd.DataFrame(columns=["Usuario", "Puntos"])

    cols_apuestas = {"Usuario", "Partido", "Goles_A", "Goles_B"}
    cols_resultados = {"Partido", "Goles_A_Real", "Goles_B_Real"}
    if not cols_apuestas.issubset(df_apuestas.columns):
        return pd.DataFrame(columns=["Usuario", "Puntos"])
    if not cols_resultados.issubset(df_resultados.columns):
        return pd.DataFrame(columns=["Usuario", "Puntos"])

    merged = df_apuestas.merge(df_resultados, on="Partido", how="inner")

    if merged.empty:
        return pd.DataFrame(columns=["Usuario", "Puntos"])

    g_a = merged["Goles_A"]
    g_b = merged["Goles_B"]
    g_a_r = merged["Goles_A_Real"]
    g_b_r = merged["Goles_B_Real"]

    exacto = (g_a == g_a_r) & (g_b == g_b_r)

    diff_apost = np.sign(g_a - g_b)
    diff_real = np.sign(g_a_r - g_b_r)
    tendencia = (diff_apost == diff_real) & ~exacto

    dif_gol_apost = g_a - g_b
    dif_gol_real = g_a_r - g_b_r
    bono_diferencia = tendencia & (dif_gol_apost == dif_gol_real)

    merged["Puntos"] = 0.0
    merged.loc[exacto, "Puntos"] = 3.0
    merged.loc[tendencia, "Puntos"] = 1.0
    merged.loc[bono_diferencia, "Puntos"] += 0.5

    leaderboard = (
        merged.groupby("Usuario")["Puntos"]
        .sum()
        .reset_index()
        .sort_values("Puntos", ascending=False)
        .reset_index(drop=True)
    )
    leaderboard.index = leaderboard.index + 1
    leaderboard.index.name = "Pos"

    return leaderboard
