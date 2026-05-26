import json
import tomllib

import gspread
from oauth2client.service_account import ServiceAccountCredentials

ALCANCE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

ID_SHEET = "1-loHkPLFild0dWPyxV0G59ryNGibyTTC9_4jXAqxA3U"

USUARIOS = [
    {"Nombre": "Joe Armada", "Pais": "España", "Bandera": "🇪🇸", "PIN": "1234"},
    {"Nombre": "Joe Gonzalez", "Pais": "España", "Bandera": "🇪🇸", "PIN": "1234"},
    {"Nombre": "Belo Armada", "Pais": "España", "Bandera": "🇪🇸", "PIN": "1234"},
    {"Nombre": "Cormac", "Pais": "España", "Bandera": "🇪🇸", "PIN": "1234"},
    {"Nombre": "Dany Gonzalez", "Pais": "Ecuador", "Bandera": "🇪🇨", "PIN": "1234"},
    {"Nombre": "Davy Gonzalez", "Pais": "Dinamarca", "Bandera": "🇩🇰", "PIN": "1234"},
    {"Nombre": "Willi Martines", "Pais": "Rusia", "Bandera": "🇷🇺", "PIN": "1234"},
    {"Nombre": "Pedrito Rodriguez", "Pais": "USA", "Bandera": "🇺🇸", "PIN": "1234"},
]

ENCABEZADOS = [["Nombre", "Pais", "Bandera", "PIN"]]


def _leer_secrets():
    with open(".streamlit/secrets.toml", "rb") as f:
        return tomllib.load(f)


def _conectar_sheets(secrets):
    creds_dict = secrets["gcp_service_account"]
    if isinstance(creds_dict, str):
        creds_dict = json.loads(creds_dict)
    credenciales = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, ALCANCE
    )
    return gspread.authorize(credenciales).open_by_key(ID_SHEET)


def main():
    secrets = _leer_secrets()
    hoja = _conectar_sheets(secrets)

    try:
        ws = hoja.worksheet("Usuarios")
    except gspread.exceptions.WorksheetNotFound:
        ws = hoja.add_worksheet(title="Usuarios", rows=200, cols=10)

    ws.clear()
    filas = ENCABEZADOS + [[u["Nombre"], u["Pais"], u["Bandera"], u["PIN"]] for u in USUARIOS]
    ws.append_rows(filas)

    print("✅ Lista de Co-fatales actualizada con éxito")


if __name__ == "__main__":
    main()
