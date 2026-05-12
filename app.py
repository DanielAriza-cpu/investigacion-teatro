import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

# 1. Configuración de carpetas y archivos
CARPETA_ANEXOS = "evidencias_investigacion"
ARCHIVO_DATOS = "registro_investigacion_unicaldas.csv"

# Crear carpeta de evidencias si no existe
if not os.path.exists(CARPETA_ANEXOS):
    os.makedirs(CARPETA_ANEXOS)  # <--- Esta línea debe tener 4 espacios o un TAB al inicio

# Función para guardar datos en el archivo CSV
def guardar_datos(dict_datos):
df = pd.DataFrame([dict_datos])
if not os.path.isfile(ARCHIVO_DATOS):
df.to_csv(ARCHIVO_DATOS, index=False, encoding='utf-8-sig')
else:
df.to_csv(ARCHIVO_DATOS, mode='a', header=False, index=False, encoding='utf-8-sig')

# 3. Interfaz de Usuario
st.set_page_config(page_title="Investigación Artes Escénicas", layout="wide", page_icon="🎭")

st.title("🏛️ Repositorio de Investigación - Artes Escénicas")
st.markdown("Universidad de Caldas | Gestión de Evidencias 2022-2026")

# Definición de pestañas
tab1, tab2, tab3 = st.tabs(["📝 Registrar Avance", "📈 Estadísticas por Grupo", "🔍 Explorador de Evidencias"])

with tab1:
st.header("Formulario de Registro")
with st.form("form_investigacion", clear_on_submit=True):
col_a, col_b = st.columns(2)
with col_a:
# --- SECCIÓN DE GRUPOS ACTUALIZADA ---
grupo_inv = st.selectbox("Grupo de Investigación", [
"Teatro, Cultura y Sociedad",
"Mundos Simbólicos: Estudios en Educación y Vida Cotidiana",
"Otro"
])
investigador = st.text_input("Nombre del Investigador/a")
proyecto = st.text_input("Título del Proyecto")

with col_b:
anio = st.select_slider("Año del reporte", options=[2022, 2023, 2024, 2025, 2026])
tipo_prod = st.multiselect("Productos", [
"Artículos", "Libros", "Capítulos de libro",
"Obras artísticas", "Certificaciones", "Ponencias", "Otros"
])
detalles = st.text_area("Eventos o detalles (Festivales, Muestras, Congresos)")

anexos = st.file_uploader("Subir evidencias (Públicas)", accept_multiple_files=True)
enviar = st.form_submit_button("Publicar Registro")

if enviar and investigador and proyecto:
archivos_subidos = []
for file in anexos:
# Guardamos con el nombre original
ruta_destino = os.path.join(CARPETA_ANEXOS, file.name)
with open(ruta_destino, "wb") as f:
f.write(file.getbuffer())
archivos_subidos.append(file.name)

# Diccionario de datos para el CSV
datos = {
"Fecha_Registro": datetime.now().strftime("%Y-%m-%d %H:%M"),
"Grupo": grupo_inv,
"Investigador": investigador,
"Proyecto": proyecto,
"Año": anio,
"Productos": ", ".join(tipo_prod),
"Archivos": ", ".join(archivos_subidos),
"Detalles": detalles
}
guardar_datos(datos)
st.success(f"✅ ¡Registro exitoso para el grupo: {grupo_inv}!")

with tab2:
st.header("Análisis de Producción")
if os.path.exists(ARCHIVO_DATOS):
df = pd.read_csv(ARCHIVO_DATOS)

c1, c2 = st.columns(2)
with c1:
st.subheader("Participación por Grupo")
fig_pie = px.pie(df, names="Grupo", hole=0.3)
st.plotly_chart(fig_pie, use_container_width=True)

with c2:
st.subheader("Evolución Temporal")
fig_bar = px.histogram(df, x="Año", color="Grupo", barmode="group")
st.plotly_chart(fig_bar, use_container_width=True)

st.write("### Tabla General de Datos")
st.dataframe(df, use_container_width=True)
else:
st.info("No hay datos registrados aún.")

with tab3:
st.header("🔍 Buscador de Evidencias y Anexos")
if os.path.exists(ARCHIVO_DATOS):
df_search = pd.read_csv(ARCHIVO_DATOS)

# Filtros interactivos
f_col1, f_col2, f_col3 = st.columns(3)
with f_col1:
sel_grupo = st.multiselect("Filtrar por Grupo", df_search["Grupo"].unique())
with f_col2:
sel_anio = st.multiselect("Filtrar por Año", df_search["Año"].unique())
with f_col3:
busq_texto = st.text_input("Buscar por nombre de archivo o palabra clave...")

# Aplicar los filtros
query = pd.Series([True] * len(df_search))
if sel_grupo: query &= df_search["Grupo"].isin(sel_grupo)
if sel_anio: query &= df_search["Año"].isin(sel_anio)

resultados = df_search[query]

# Listado de resultados
for idx, fila in resultados.iterrows():
if pd.notna(fila['Archivos']):
lista_files = fila['Archivos'].split(", ")
for arc in lista_files:
if busq_texto.lower() in arc.lower() or busq_texto == "":
with st.expander(f"📄 {arc} | {fila['Grupo']}"):
st.write(f"**Investigador/a:** {fila['Investigador']}")
st.write(f"**Proyecto:** {fila['Proyecto']} ({fila['Año']})")

path = os.path.join(CARPETA_ANEXOS, arc)
if os.path.exists(path):
with open(path, "rb") as file_bytes:
st.download_button("Descargar Evidencia", file_bytes, file_name=arc, key=f"{arc}_{idx}")
else:
st.warning("La base de datos está vacía.")
