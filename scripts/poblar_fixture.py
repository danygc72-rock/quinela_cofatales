import json
import tomllib

import gspread
from oauth2client.service_account import ServiceAccountCredentials

ALCANCE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

ID_SHEET = "1-loHkPLFild0dWPyxV0G59ryNGibyTTC9_4jXAqxA3U"

DATOS_FIXTURE = [
    [1, "Mexico", "South Africa", "2026-06-11 14:00:00", "Pendiente"],
    [2, "South Korea", "Czech Republic", "2026-06-11 21:00:00", "Pendiente"],
    [3, "Canada", "Bosnia and Herzegovina", "2026-06-12 14:00:00", "Pendiente"],
    [4, "United States", "Paraguay", "2026-06-12 20:00:00", "Pendiente"],
    [5, "Qatar", "Switzerland", "2026-06-13 14:00:00", "Pendiente"],
    [6, "Brazil", "Morocco", "2026-06-13 17:00:00", "Pendiente"],
    [7, "Haiti", "Scotland", "2026-06-13 20:00:00", "Pendiente"],
    [8, "Australia", "Türkiye", "2026-06-13 23:00:00", "Pendiente"],
    [9, "Germany", "Curaçao", "2026-06-14 12:00:00", "Pendiente"],
    [10, "Netherlands", "Japan", "2026-06-14 15:00:00", "Pendiente"],
    [11, "Ivory Coast", "Ecuador", "2026-06-14 18:00:00", "Pendiente"],
    [12, "Sweden", "Tunisia", "2026-06-14 21:00:00", "Pendiente"],
    [13, "Spain", "Cape Verde", "2026-06-15 11:00:00", "Pendiente"],
    [14, "Belgium", "Egypt", "2026-06-15 14:00:00", "Pendiente"],
    [15, "Saudi Arabia", "Uruguay", "2026-06-15 17:00:00", "Pendiente"],
]

HEADERS = [["ID", "Equipo_A", "Equipo_B", "Fecha_Limite", "Estado"]]


def conectar():
    with open(".streamlit/secrets.toml", "rb") as f:
        secrets = tomllib.load(f)

    creds_dict = secrets["gcp_service_account"]
    if isinstance(creds_dict, str):
        creds_dict = json.loads(creds_dict)

    credenciales = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, ALCANCE
    )
    cliente = gspread.authorize(credenciales)
    return cliente.open_by_key(ID_SHEET)


def main():
    try:
        hoja = conectar()
    except FileNotFoundError:
        print("No se encontró .streamlit/secrets.toml")
        return
    except Exception as e:
        print(f"Error de conexión: {e}")
        return

    try:
        ws = hoja.worksheet("Fixture")
    except Exception:
        ws = hoja.add_worksheet(title="Fixture", rows=200, cols=10)

    ws.clear()
    ws.append_rows(HEADERS + DATOS_FIXTURE)

    print(f"Fixture poblado con {len(DATOS_FIXTURE)} partidos.")


if __name__ == "__main__":
    main()
