import os

ALCANCE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

ID_SHEET = os.getenv("ID_SHEET", "1-loHkPLFild0dWPyxV0G59ryNGibyTTC9_4jXAqxA3U")

COLUMNAS_APUESTAS = ["Nombre", "Equipo A", "Equipo B", "Goles A", "Goles B"]
COLUMNAS_RESULTADOS = ["Equipo A", "Equipo B", "Goles A", "Goles B"]

PUNTAJE_EXACTO = 3
PUNTAJE_GANADOR = 1

USUARIOS_PERMITIDOS = [
    "Selecciona tu nombre...",
    "Joe Armada",
    "Joe Gonzalez",
    "Davy Gonzalez",
    "Pedrito Rodriguez",
    "Belo Armada",
    "Willi Martinez",
    "Dani Gonzalez",
    "Cormac",
]

PARTIDOS_FIXTURE = [
    {"partido": "Selecciona un partido...", "limite": None},
    {"partido": "México vs Sudáfrica (Amistoso de Prueba)", "limite": "2026-07-10 10:00:00"},
    {"partido": "Argentina vs Colombia", "limite": "2026-07-12 15:00:00"},
    {"partido": "España vs Alemania", "limite": "2026-07-15 21:00:00"},
]
