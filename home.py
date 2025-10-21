#Por Alfonso Espinoza Chevez

import streamlit as st
import pandas as pd
import requests
import numpy as np
import random
import plotly.express as px

st.set_page_config(page_title="Dashboard Usuarios", page_icon="📊", layout="wide")

st.title("🌐 GUIA PRACTICA")

# --- 1. Cargar datos desde la API ---
url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)
if response.status_code != 200:
    st.error("❌ No se pudo conectar con la API.")
    st.stop()

data = response.json()
df = pd.DataFrame(data)

# --- 2. Normalizar campos anidados ---
address_df = pd.json_normalize(df["address"]).add_prefix("address_")
company_df = pd.json_normalize(df["company"]).add_prefix("company_")
df = pd.concat([df.drop(columns=["address", "company"]), address_df, company_df], axis=1)

# --- 3. Crear columna simulada 'monto' para métricas ---
df["monto"] = [random.randint(1000, 10000) for _ in range(len(df))]  # simulación de montos

# --- 4. Barra lateral: filtros ---
st.sidebar.header("🎛️ Filtros dinámicos")

# Filtro por ciudad
cities = ["Todas"] + sorted(df["address_city"].unique().tolist())
selected_city = st.sidebar.selectbox("Ciudad", cities)

# Filtro por empresa
companies = ["Todas"] + sorted(df["company_name"].unique().tolist())
selected_company = st.sidebar.selectbox("Empresa", companies)

# Filtro por nombre
search_name = st.sidebar.text_input("Buscar por nombre")

# --- 5. Aplicar filtros ---
filtered_df = df.copy()

if selected_city != "Todas":
    filtered_df = filtered_df[filtered_df["address_city"] == selected_city]
if selected_company != "Todas":
    filtered_df = filtered_df[filtered_df["company_name"] == selected_company]
if search_name:
    filtered_df = filtered_df[filtered_df["name"].str.contains(search_name, case=False, na=False)]

# --- 6. Mostrar tabla filtrada ---
st.subheader("📋 Resultados filtrados")
st.write(f"**Total de usuarios encontrados:** {len(filtered_df)}")
st.dataframe(filtered_df[["id", "name", "email", "address_city", "company_name", "monto"]])

# --- 7. Gráficos de distribución ---
st.subheader("📈 Distribución de usuarios por ciudad")
if not filtered_df.empty:
    st.bar_chart(filtered_df["address_city"].value_counts())
else:
    st.warning("No hay usuarios que coincidan con los filtros seleccionados.")

st.subheader("📈 Distribución de usuarios por empresa")
if not filtered_df.empty:
    st.bar_chart(filtered_df["company_name"].value_counts())

# --- 8. KPIs y análisis descriptivo ---
st.header("🏷️ KPIs y estadísticas descriptivas")

total_registros = len(filtered_df)
total_monto = filtered_df["monto"].sum()
promedio_monto = filtered_df["monto"].mean()
max_monto = filtered_df["monto"].max()
min_monto = filtered_df["monto"].min()

col1, col2, col3 = st.columns(3)
col1.metric("Total usuarios", total_registros)
col2.metric("Monto total simulado", f"${total_monto}")
col3.metric("Promedio por usuario", f"${promedio_monto:.2f}")

col4, col5 = st.columns(2)
col4.metric("Monto máximo", f"${max_monto}")
col5.metric("Monto mínimo", f"${min_monto}")

st.subheader("📊 Estadísticas descriptivas del 'monto'")
st.dataframe(filtered_df["monto"].describe())


 

# --- 9. Visualizaciones interactivas ---
st.header("📊 Visualizaciones interactivas")

# a) Barras por tipo (empresa)
st.subheader("Usuarios por empresa (barra)")
fig_bar = px.bar(
    filtered_df.groupby("company_name").size().reset_index(name="count"),
    x="company_name",
    y="count",
    color="company_name",
    title="Número de usuarios por empresa"
)
st.plotly_chart(fig_bar, use_container_width=True)

# b) Línea mensual (simulada)
# Creamos columna 'month' aleatoria
filtered_df["month"] = [random.randint(1,12) for _ in range(len(filtered_df))]
df_monthly = filtered_df.groupby("month")["monto"].sum().reset_index()

st.subheader("Monto total por mes (simulado)")
fig_line = px.line(
    df_monthly,
    x="month",
    y="monto",
    markers=True,
    title="Monto total por mes"
)
st.plotly_chart(fig_line, use_container_width=True)

# c) Barras apiladas tipo × mes
st.subheader("Monto por empresa y mes (barras apiladas)")
df_stack = filtered_df.groupby(["month", "company_name"])["monto"].sum().reset_index()
fig_stack = px.bar(
    df_stack,
    x="month",
    y="monto",
    color="company_name",
    barmode="stack",
    title="Monto apilado por empresa y mes"
)
st.plotly_chart(fig_stack, use_container_width=True)

# d) Pastel por proporción de contratos (usuarios por empresa)
st.subheader("Proporción de usuarios por empresa (pastel)")
fig_pie = px.pie(
    filtered_df.groupby("company_name").size().reset_index(name="count"),
    values="count",
    names="company_name",
    title="Proporción de usuarios por empresa"
)
st.plotly_chart(fig_pie, use_container_width=True)


# --- 10. Diagrama de dispersión: Monto vs Contratos ---
st.header("💠 Relación entre Monto y Cantidad de Contratos")

# Simulamos columna 'contracts'
filtered_df["contracts"] = [random.randint(1, 20) for _ in range(len(filtered_df))]

# internal_type será company_name
filtered_df["internal_type"] = filtered_df["company_name"]

# Crear scatter plot
fig_scatter = px.scatter(
    filtered_df,
    x="contracts",
    y="monto",
    color="internal_type",
    size="monto",
    hover_data=["name", "email"],
    title="Monto Total vs Cantidad de Contratos (simulado)"
)
st.plotly_chart(fig_scatter, use_container_width=True)


# --- 11. Comparativa de Tipos de Contratación por Mes ---
st.header("📈 Comparativa de Tipos de Contratación por Mes")

# Asegurarnos de tener columna 'month' (ya se creó antes, si no, la creamos)
if "month" not in filtered_df.columns:
    filtered_df["month"] = [random.randint(1,12) for _ in range(len(filtered_df))]

# internal_type será company_name
filtered_df["internal_type"] = filtered_df["company_name"]

# Agrupamos por mes e internal_type y sumamos montos
df_line = filtered_df.groupby(["month", "internal_type"])["monto"].sum().reset_index()

# Gráfico de líneas
fig_line_type = px.line(
    df_line,
    x="month",
    y="monto",
    color="internal_type",
    markers=True,
    title="Comportamiento mensual de 'monto' por tipo de empresa",
    labels={"month": "Mes", "monto": "Monto Total", "internal_type": "Empresa"}
)
st.plotly_chart(fig_line_type, use_container_width=True)

# Breve interpretación debajo
st.markdown("""
**Interpretación:**  
Este gráfico muestra la evolución del monto total simulado por empresa a lo largo de los meses.  
Se puede observar qué empresas (tipos) concentran mayor monto en ciertos meses y comparar su comportamiento relativo.
""")





st.header("📊 12- Análisis por Años")

# --- 1. Asegurarnos de tener columna 'year' ---
if "year" not in filtered_df.columns:
    filtered_df["year"] = [random.choice([2022, 2023, 2024]) for _ in range(len(filtered_df))]

# internal_type será company_name
filtered_df["internal_type"] = filtered_df["company_name"]

# --- 2. KPIs por año ---
st.subheader("🏷️ KPIs por año")
kpis_year = filtered_df.groupby("year")["monto"].agg(["count","sum","mean","max","min"]).reset_index()
st.dataframe(kpis_year)

# --- 3. Barras apiladas tipo × año ---
st.subheader("📊 Montos por empresa y año (barras apiladas)")
df_stack_year = filtered_df.groupby(["year","internal_type"])["monto"].sum().reset_index()
fig_stack_year = px.bar(
    df_stack_year,
    x="year",
    y="monto",
    color="internal_type",
    barmode="stack",
    title="Monto total por empresa y año"
)
st.plotly_chart(fig_stack_year, use_container_width=True)

# --- 4. Evolución mensual comparada ---
st.subheader("📈 Evolución mensual comparada por año")
df_line_year = filtered_df.groupby(["year","month"])["monto"].sum().reset_index()
fig_line_year = px.line(
    df_line_year,
    x="month",
    y="monto",
    color="year",
    markers=True,
    title="Monto mensual por año",
    labels={"month":"Mes","monto":"Monto total","year":"Año"}
)
st.plotly_chart(fig_line_year, use_container_width=True)

# --- 5. Heatmap año × mes ---
st.subheader("🌡️ Heatmap año × mes")
heatmap_df = df_line_year.pivot(index="year", columns="month", values="monto")
fig_heatmap = px.imshow(
    heatmap_df,
    labels={"x":"Mes","y":"Año","color":"Monto"},
    text_auto=True,
    aspect="auto",
    title="Mapa de calor de monto por año y mes"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# --- 6. Interpretación ---
st.markdown("""
**Interpretación:**  
- Podemos comparar los montos por año y detectar picos o caídas simuladas.  
- Barras apiladas muestran qué empresas contribuyen más al total en cada año.  
- La línea mensual permite ver tendencias y variabilidad mes a mes.  
- El heatmap facilita identificar meses con mayor actividad o concentración de monto.
""")






st.header("💾 13- Exportar Resultados")

# Convertir DataFrame filtrado a CSV
csv = filtered_df.to_csv(index=False).encode("utf-8")

# Botón de descarga
st.download_button(
    label="Descargar datos filtrados como CSV",
    data=csv,
    file_name="usuarios_filtrados.csv",
    mime="text/csv"
)
