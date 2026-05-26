import json
import tomllib
from datetime import datetime

import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials

ALCANCE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

ID_SHEET = "1-loHkPLFild0dWPyxV0G59ryNGibyTTC9_4jXAqxA3U"

HEADERS = [["ID", "Equipo_A", "Equipo_B", "Fecha_Limite", "Estado", "Goles_A_Real", "Goles_B_Real"]]


def leer_secrets():
    with open(".streamlit/secrets.toml", "rb") as f:
        return tomllib.load(f)


def conectar_sheets(secrets):
    creds_dict = secrets["gcp_service_account"]
    if isinstance(creds_dict, str):
        creds_dict = json.loads(creds_dict)
    credenciales = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, ALCANCE
    )
    return gspread.authorize(credenciales).open_by_key(ID_SHEET)


def obtener_partidos_api(api_key):
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": api_key}
    respuesta = requests.get(url, headers=headers, timeout=15)

    if respuesta.status_code == 403:
        print(
            "La API de football-data.org devolvió 403 (acceso denegado). "
            "El plan gratuito no tiene acceso al Mundial 2026. "
            "Usá 'python scripts/poblar_fixture.py' con los datos manuales."
        )
        return None

    if respuesta.status_code != 200:
        print(f"Error de API: código {respuesta.status_code}")
        return None

    return respuesta.json()


def transformar_partidos(data):
    filas = []
    for i, match in enumerate(data["matches"], start=1):
        equipo_a = match["homeTeam"]["name"] or "Por definir"
        equipo_b = match["awayTeam"]["name"] or "Por definir"

        utc = match["utcDate"]
        fecha_local = (
            datetime.fromisoformat(utc.replace("Z", "+00:00"))
            .strftime("%Y-%m-%d %H:%M:%S")
        )

        if match["status"] == "FINISHED":
            estado = "Terminado"
            goles_a = match["score"]["fullTime"]["home"]
            goles_b = match["score"]["fullTime"]["away"]
        else:
            estado = "Pendiente"
            goles_a = ""
            goles_b = ""

        filas.append([i, equipo_a, equipo_b, fecha_local, estado, goles_a, goles_b])

    return filas


def main():
    try:
        secrets = leer_secrets()
    except FileNotFoundError:
        print("No se encontró .streamlit/secrets.toml")
        return

    api_key = secrets.get("FOOTBALL_API_KEY")
    if not api_key:
        print("FOOTBALL_API_KEY no está configurada en secrets.toml")
        return

    print("Consultando API de football-data.org...")
    data = obtener_partidos_api(api_key)
    if data is None:
        return

    partidos = transformar_partidos(data)
    print(f"Obtenidos {len(partidos)} partidos de la API.")

    try:
        hoja = conectar_sheets(secrets)
    except Exception as e:
        print(f"Error conectando a Google Sheets: {e}")
        return

    try:
        ws = hoja.worksheet("Fixture")
    except Exception:
        ws = hoja.add_worksheet(title="Fixture", rows=400, cols=10)

    ws.clear()
    ws.append_rows(HEADERS + partidos)

    print(f"Fixture actualizado con {len(partidos)} partidos en Google Sheets.")


if __name__ == "__main__":
    main()
