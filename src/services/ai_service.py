import streamlit as st
from google import genai


def obtener_prediccion(partido):
    api_key = st.secrets.get("GEMINI_API_KEY") or None
    if not api_key:
        raise ConnectionError("GEMINI_API_KEY no configurada en secrets.")
    try:
        cliente = genai.Client(api_key=api_key)
    except Exception as e:
        raise ConnectionError(f"No se pudo conectar con Gemini: {e}")

    prompt = (
        "Actuás como un experto analista de fútbol con un tono sarcástico y directo. "
        f"Hacé un análisis rápido de máximo 2 párrafos para el partido: {partido}. "
        "Mencioná quién es el favorito de forma objetiva, pero incluí una burla sutil "
        "sobre la mala suerte de apostar en contra de la estadística. "
        "Dirigite a un grupo de amigos llamado 'Los Co-fatales'. "
        "Terminá con un marcador probable."
    )

    modelos = ["gemini-2.0-flash-lite", "gemini-2.5-flash", "gemini-2.0-flash"]
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
