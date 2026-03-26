import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, array_contains, count, desc

st.set_page_config(
    page_title="Biblia NTV — Análisis ETL",
    page_icon="📖",
    layout="wide"
)

st.title("Análisis ETL — Biblia NTV")
st.markdown("Análisis de frecuencia de palabras clave con Apache Spark")

# ── SparkSession ──────────────────────────────────────────────────────────────
@st.cache_resource
def get_spark():
    return SparkSession.builder \
        .appName("Streamlit_Biblia") \
        .master("local[*]") \
        .config("spark.ui.port", "4041") \
        .getOrCreate()

# ── Cargar datos ──────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    spark = get_spark()
    df = spark.read.parquet(
        "/opt/notebooks/proyecto/data/biblia_ntv_procesada.parquet"
    )
    return df.select(
    "libro", "capitulo", "verso", "texto", "num_palabras"   # ← verso, no versiculo
    ).toPandas()

# ── UI ────────────────────────────────────────────────────────────────────────
with st.spinner("Cargando datos desde Parquet..."):
    df = cargar_datos()

st.success(f"Dataset cargado: {len(df):,} versículos")

# Sidebar
st.sidebar.header("Filtros")
palabra = st.sidebar.text_input("Buscar palabra", value="esperanza")
libro_sel = st.sidebar.selectbox(
    "Filtrar por libro",
    ["Todos"] + sorted(df["libro"].unique().tolist())
)

# Filtrar
df_filtrado = df[df["texto"].str.contains(palabra, case=False, na=False)]
if libro_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["libro"] == libro_sel]

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Versículos encontrados", f"{len(df_filtrado):,}")
col2.metric("Libros con la palabra",  f"{df_filtrado['libro'].nunique()}")
col3.metric("% del corpus",           f"{len(df_filtrado)/len(df)*100:.2f}%")

# Tabla
st.subheader(f"Versículos con «{palabra}»")
st.dataframe(df_filtrado[["libro","capitulo","verso","texto"]], use_container_width=True)

# Gráfico
st.subheader("Frecuencia por libro")
freq = df_filtrado.groupby("libro").size().sort_values(ascending=False).head(15)
st.bar_chart(freq)