{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww15140\viewh13300\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
import os\
import plotly.express as px\
from datetime import datetime\
\
# 1. Configuraci\'f3n de carpetas y archivos\
CARPETA_ANEXOS = "evidencias_investigacion"\
ARCHIVO_DATOS = "registro_investigacion_unicaldas.csv"\
\
# Crear carpeta de evidencias si no existe\
if not os.path.exists(CARPETA_ANEXOS):\
    os.makedirs(CARPETA_ANEXOS)\
\
# Funci\'f3n para guardar datos en el archivo CSV\
def guardar_datos(dict_datos):\
    df = pd.DataFrame([dict_datos])\
    if not os.path.isfile(ARCHIVO_DATOS):\
        df.to_csv(ARCHIVO_DATOS, index=False, encoding='utf-8-sig')\
    else:\
        df.to_csv(ARCHIVO_DATOS, mode='a', header=False, index=False, encoding='utf-8-sig')\
\
# 3. Interfaz de Usuario\
st.set_page_config(page_title="Investigaci\'f3n Artes Esc\'e9nicas", layout="wide", page_icon="\uc0\u55356 \u57261 ")\
\
st.title("\uc0\u55356 \u57307 \u65039  Repositorio de Investigaci\'f3n - Artes Esc\'e9nicas")\
st.markdown("Universidad de Caldas | Gesti\'f3n de Evidencias 2022-2026")\
\
# Definici\'f3n de pesta\'f1as\
tab1, tab2, tab3 = st.tabs(["\uc0\u55357 \u56541  Registrar Avance", "\u55357 \u56520  Estad\'edsticas por Grupo", "\u55357 \u56589  Explorador de Evidencias"])\
\
with tab1:\
    st.header("Formulario de Registro")\
    with st.form("form_investigacion", clear_on_submit=True):\
        col_a, col_b = st.columns(2)\
        with col_a:\
            # --- SECCI\'d3N DE GRUPOS ACTUALIZADA ---\
            grupo_inv = st.selectbox("Grupo de Investigaci\'f3n", [\
                "Teatro, Cultura y Sociedad", \
                "Mundos Simb\'f3licos: Estudios en Educaci\'f3n y Vida Cotidiana", \
                "Otro"\
            ])\
            investigador = st.text_input("Nombre del Investigador/a")\
            proyecto = st.text_input("T\'edtulo del Proyecto")\
            \
        with col_b:\
            anio = st.select_slider("A\'f1o del reporte", options=[2022, 2023, 2024, 2025, 2026])\
            tipo_prod = st.multiselect("Productos", [\
                "Art\'edculos", "Libros", "Cap\'edtulos de libro", \
                "Obras art\'edsticas", "Certificaciones", "Ponencias", "Otros"\
            ])\
            detalles = st.text_area("Eventos o detalles (Festivales, Muestras, Congresos)")\
            \
        anexos = st.file_uploader("Subir evidencias (P\'fablicas)", accept_multiple_files=True)\
        enviar = st.form_submit_button("Publicar Registro")\
\
    if enviar and investigador and proyecto:\
        archivos_subidos = []\
        for file in anexos:\
            # Guardamos con el nombre original\
            ruta_destino = os.path.join(CARPETA_ANEXOS, file.name)\
            with open(ruta_destino, "wb") as f:\
                f.write(file.getbuffer())\
            archivos_subidos.append(file.name)\
        \
        # Diccionario de datos para el CSV\
        datos = \{\
            "Fecha_Registro": datetime.now().strftime("%Y-%m-%d %H:%M"),\
            "Grupo": grupo_inv,\
            "Investigador": investigador,\
            "Proyecto": proyecto,\
            "A\'f1o": anio,\
            "Productos": ", ".join(tipo_prod),\
            "Archivos": ", ".join(archivos_subidos),\
            "Detalles": detalles\
        \}\
        guardar_datos(datos)\
        st.success(f"\uc0\u9989  \'a1Registro exitoso para el grupo: \{grupo_inv\}!")\
\
with tab2:\
    st.header("An\'e1lisis de Producci\'f3n")\
    if os.path.exists(ARCHIVO_DATOS):\
        df = pd.read_csv(ARCHIVO_DATOS)\
        \
        c1, c2 = st.columns(2)\
        with c1:\
            st.subheader("Participaci\'f3n por Grupo")\
            fig_pie = px.pie(df, names="Grupo", hole=0.3)\
            st.plotly_chart(fig_pie, use_container_width=True)\
            \
        with c2:\
            st.subheader("Evoluci\'f3n Temporal")\
            fig_bar = px.histogram(df, x="A\'f1o", color="Grupo", barmode="group")\
            st.plotly_chart(fig_bar, use_container_width=True)\
            \
        st.write("### Tabla General de Datos")\
        st.dataframe(df, use_container_width=True)\
    else:\
        st.info("No hay datos registrados a\'fan.")\
\
with tab3:\
    st.header("\uc0\u55357 \u56589  Buscador de Evidencias y Anexos")\
    if os.path.exists(ARCHIVO_DATOS):\
        df_search = pd.read_csv(ARCHIVO_DATOS)\
        \
        # Filtros interactivos\
        f_col1, f_col2, f_col3 = st.columns(3)\
        with f_col1:\
            sel_grupo = st.multiselect("Filtrar por Grupo", df_search["Grupo"].unique())\
        with f_col2:\
            sel_anio = st.multiselect("Filtrar por A\'f1o", df_search["A\'f1o"].unique())\
        with f_col3:\
            busq_texto = st.text_input("Buscar por nombre de archivo o palabra clave...")\
\
        # Aplicar los filtros\
        query = pd.Series([True] * len(df_search))\
        if sel_grupo: query &= df_search["Grupo"].isin(sel_grupo)\
        if sel_anio: query &= df_search["A\'f1o"].isin(sel_anio)\
            \
        resultados = df_search[query]\
\
        # Listado de resultados\
        for idx, fila in resultados.iterrows():\
            if pd.notna(fila['Archivos']):\
                lista_files = fila['Archivos'].split(", ")\
                for arc in lista_files:\
                    if busq_texto.lower() in arc.lower() or busq_texto == "":\
                        with st.expander(f"\uc0\u55357 \u56516  \{arc\} | \{fila['Grupo']\}"):\
                            st.write(f"**Investigador/a:** \{fila['Investigador']\}")\
                            st.write(f"**Proyecto:** \{fila['Proyecto']\} (\{fila['A\'f1o']\})")\
                            \
                            path = os.path.join(CARPETA_ANEXOS, arc)\
                            if os.path.exists(path):\
                                with open(path, "rb") as file_bytes:\
                                    st.download_button("Descargar Evidencia", file_bytes, file_name=arc, key=f"\{arc\}_\{idx\}")\
    else:\
        st.warning("La base de datos est\'e1 vac\'eda.")}