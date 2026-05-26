import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
from src.config import ID_SHEET, ALCANCE


@st.cache_resource
def conectar_google_sheets():
    try:
        if "gcp_service_account" in st.secrets:
            creds_dict = st.secrets["gcp_service_account"]
            if isinstance(creds_dict, str):
                creds_dict = json.loads(creds_dict)
            credenciales = ServiceAccountCredentials.from_json_keyfile_dict(
                creds_dict, ALCANCE
            )
        else:
            credenciales = ServiceAccountCredentials.from_json_keyfile_name(
                "credenciales.json", ALCANCE
            )
        cliente = gspread.authorize(credenciales)
        hoja = cliente.open_by_key(ID_SHEET)
        return hoja
    except FileNotFoundError:
        st.error("No se encontró el archivo de credenciales.")
        return None
    except Exception as e:
        st.error(f"Error conectando con Google Sheets: {e}")
        return None


def obtener_datos_hoja(hoja, nombre_pestana="Apuestas"):
    try:
        pestana = hoja.worksheet(nombre_pestana)
        return pestana.get_all_records()
    except Exception as e:
        st.error(f"Error leyendo datos de '{nombre_pestana}': {e}")
        return []


def agregar_fila(hoja, datos, nombre_pestana="Apuestas"):
    try:
        pestana = hoja.worksheet(nombre_pestana)
        pestana.append_row(datos)
        return True
    except Exception as e:
        st.error(f"Error agregando fila: {e}")
        return False
