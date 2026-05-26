import streamlit as st
from google import genai


def _formatear_ranking(ranking_df):
    if ranking_df is None or ranking_df.empty:
        return ""
    lineas = []
    for i, (_, row) in enumerate(ranking_df.iterrows(), start=1):
        lineas.append(
            f"{i}. {row['Usuario']} - {int(row['Puntos'])} pts "
            f"({int(row['Exactos'])} exactos)"
        )
    return "\n".join(lineas)


def _construir_prompt(partidos_txt, ranking_txt):
    prompt = (
        "Actuás como 'El Oráculo de los Co-fatales', un experto en fútbol "
        "con un ego gigante, cínico y que habla con jerga cubana pesada. "
        "Usás frases como: asere, que volá, tremendo paquete, estás en candela, "
        "no me vengas con cuentos, fundío, especulador, acere, mi socio, "
        "esto está mas claro que el agua de coco, dale bolá.\n\n"
        f"Analizá los siguientes partidos de la jornada: {partidos_txt}\n"
        f"Máximo 2 párrafos por partido. "
        "Separá cada análisis con '---'. "
        "Terminá cada uno con 'Marcador Probable: X - Y'.\n"
        "Mencioná quién es el favorito y burlate de los que apuesten por el rival.\n"
    )
    if ranking_txt:
        prompt += (
            f"Este es el ranking actual de Los Co-fatales para que te burles "
            f"de los que van últimos (menciónalos por nombre):\n{ranking_txt}\n"
            "Burlate especialmente del último, decile que se retire.\n"
        )
    return prompt


def obtener_prediccion_oraculo(partidos_txt, ranking_df=None):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        raise ConnectionError("GEMINI_API_KEY no configurada en secrets.")

    try:
        cliente = genai.Client(api_key=api_key)
    except Exception as e:
        raise ConnectionError(f"No se pudo conectar con Gemini: {e}")

    ranking_txt = _formatear_ranking(ranking_df)
    prompt = _construir_prompt(partidos_txt, ranking_txt)

    modelos = ["gemini-2.5-flash-lite", "gemini-flash-lite-latest", "gemini-2.5-flash"]
    ultimo_error = None

    for modelo in modelos:
        try:
            respuesta = cliente.models.generate_content(
                model=modelo,
                contents=prompt,
            )
            return respuesta.text
        except Exception as e:
            ultimo_error = e
            continue

    mensaje = str(ultimo_error)
    if "RESOURCE_EXHAUSTED" in mensaje or "quota" in mensaje.lower():
        raise RuntimeError("La IA está agotada por hoy. Probá más tarde.")
    raise RuntimeError(f"Error al obtener predicción: {mensaje}")
