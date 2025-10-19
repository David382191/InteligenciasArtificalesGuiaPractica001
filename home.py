#Por Alfonso Espinoza Chevez
import pandas as pd
import requests
import streamlit as st


#DB_NAME = 'usuarios3.db'
API_URL = 'https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/get_analysis'

response = requests.get(API_URL, timeout=20)
if response.status_code != 200:
    raise SystemExit(f'❌ Error al consumir la API ({response.status_code})')
users = response.json()
print(f'Filas recibidas: {len(users)}')
users[:2]  # vista rápida

# =========================
# 🧰 CONFIGURACIÓN INICIAL
# =========================
st.set_page_config(page_title="Contrataciones Públicas", layout="wide")
st.title("📊 Análisis de Contrataciones Públicas - Ecuador")

# =========================
# 🧭 FILTROS EN SIDEBAR
# =========================
st.sidebar.header("Filtros")
year = st.sidebar.slider("Año", min_value=2015, max_value=2025, value=2025)
region = st.sidebar.selectbox("Provincia", ["Pichincha", "Guayas", "Azuay", "Manabí"])
tipo = st.sidebar.selectbox("Tipo de Contratación", ["Bienes", "Obras", "Servicios"])
buscar = st.sidebar.button("🔍 Buscar datos")

