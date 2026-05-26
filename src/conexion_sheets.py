import json
from datetime import datetime, timezone

import gspread
import pandas as pd
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


@st.cache_data(ttl=300)
def obtener_proximos_partidos():
    hoja = conectar_google_sheets()
    if not hoja:
        return []
    try:
        registros = hoja.worksheet("Fixture").get_all_records()
        df = pd.DataFrame(registros)
        df["Fecha_Limite"] = pd.to_datetime(df["Fecha_Limite"]).dt.tz_localize("UTC")

        ahora_utc = datetime.now(timezone.utc)
        df = df[df["Fecha_Limite"] >= ahora_utc].copy()
        df = df.sort_values("Fecha_Limite")
        dos_dias = df["Fecha_Limite"].dt.date.iloc[0] + pd.Timedelta(days=1) if not df.empty else None
        if dos_dias is not None:
            df = df[df["Fecha_Limite"].dt.date <= dos_dias]
        df["hora_utc"] = df["Fecha_Limite"].dt.strftime("%H:%M")
        df["fecha_utc"] = df["Fecha_Limite"].dt.strftime("%Y-%m-%d")
        df["fecha_legible"] = df["Fecha_Limite"].dt.strftime("%d %b %Y")
        return df.to_dict(orient="records")
    except Exception:
        return []


@st.cache_data(ttl=300)
def obtener_partidos_activos():
    hoja = conectar_google_sheets()
    if not hoja:
        return []
    try:
        registros = hoja.worksheet("Fixture").get_all_records()
        df = pd.DataFrame(registros)
        df["Fecha_Limite"] = (
            pd.to_datetime(df["Fecha_Limite"])
            .dt.tz_localize("UTC")
        )

        ahora_utc = datetime.now(timezone.utc)
        df = df[
            (df["Fecha_Limite"].dt.date == ahora_utc.date())
            & (df["Fecha_Limite"] > ahora_utc)
            & (df["Estado"] != "Terminado")
        ]
        df["hora_utc"] = df["Fecha_Limite"].dt.strftime("%H:%M")
        df["fecha_utc"] = df["Fecha_Limite"].dt.strftime("%Y-%m-%d %H:%M")
        return df.to_dict(orient="records")
    except Exception:
        return []


def obtener_datos_hoja(hoja, nombre_pestana="Apuestas"):
    try:
        pestana = hoja.worksheet(nombre_pestana)
        return pestana.get_all_records()
    except Exception as e:
        st.error(f"Error leyendo datos de '{nombre_pestana}': {e}")
        return []


@st.cache_data(ttl=600)
def obtener_usuarios():
    hoja = conectar_google_sheets()
    if not hoja:
        return pd.DataFrame(columns=["Nombre", "Pais", "Bandera", "PIN"])
    try:
        registros = hoja.worksheet("Usuarios").get_all_records()
        return pd.DataFrame(registros)
    except Exception:
        return pd.DataFrame(columns=["Nombre", "Pais", "Bandera", "PIN"])


def agregar_fila(hoja, datos, nombre_pestana="Apuestas"):
    try:
        pestana = hoja.worksheet(nombre_pestana)
        pestana.append_row(datos)
        return True
    except Exception as e:
        st.error(f"Error agregando fila: {e}")
        return False
