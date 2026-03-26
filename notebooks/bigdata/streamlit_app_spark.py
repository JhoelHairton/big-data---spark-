import streamlit as st
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pathlib import Path

# 1. Recursos pesados cacheados: SparkSession + modelo
@st.cache_resource
def get_spark():
    return (
        SparkSession.builder
        .appName("pima-diabetes-streamlit-spark")
        .master("local[*]")
        .getOrCreate()
    )

@st.cache_resource
def load_model():
    model_path = Path("artefactos") / "modelo_spark_pima"
    if not model_path.exists():
        raise FileNotFoundError(
            f"No se encontró el modelo Spark en {model_path}. "
            "Primero ejecuta `train_pima_spark.py`."
        )
    return PipelineModel.load(str(model_path))

# Intentar cargar recursos
try:
    spark = get_spark()
    modelo = load_model()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

# 2. Título y descripción
st.title("🤖 Predicción de Diabetes (Pima Dataset) — Versión Spark")

st.write(
    "Ingrese los valores clínicos para predecir si la paciente "
    "probablemente tiene diabetes. "
    "En este demo el modelo de clasificación fue entrenado con **Apache Spark MLlib**."
)

# 3. Ingreso de datos del paciente (mismos sliders que sklearn)
npreg = st.slider("Número de embarazos", 0, 20, 2)
glu   = st.slider("Nivel de glucosa (mg/dl)", 50, 200, 100)
bp    = st.slider("Presión arterial (mmHg)", 40, 130, 70)
skin  = st.slider("Espesor del pliegue cutáneo (mm)", 7, 100, 20)
bmi   = st.slider("IMC", 10.0, 50.0, 25.0)
ped   = st.slider("Pedigree de diabetes", 0.0, 2.5, 0.5)
age   = st.slider("Edad (años)", 18, 90, 35)

# 4. Predicción con Spark
if st.button("Predecir (Spark)"):
    # Crear DataFrame Spark de una fila
    input_df = spark.createDataFrame(
        [(npreg, glu, bp, skin, bmi, ped, age)],
        ["npreg", "glu", "bp", "skin", "bmi", "ped", "age"]
    )

    result = (
        modelo
        .transform(input_df)
        .select("probability", "prediction")
        .collect()[0]
    )

    # probability es un vector [p0, p1]; p1 = prob. clase positiva
    prob = float(result["probability"][1])
    pred = int(result["prediction"])   # 0 = No diabética, 1 = Diabética

    resultado = "Diabética" if pred == 1 else "No diabética"

    st.markdown(f"### Resultado: **{resultado}**")
    st.write(f"Probabilidad estimada de diabetes: **{prob:.2%}**")
    st.caption("Demo educativa con Spark MLlib. No usar para diagnóstico real.")

# 5. Info en sidebar (igual estilo que sklearn)
st.sidebar.title("ℹ️ Sobre esta versión (Spark)")
st.sidebar.write(
    "- Dataset: Pima.tr (MASS)\n"
    "- Motor: Apache Spark MLlib\n"
    "- Modelo: LogisticRegression (Spark)\n"
    "- Script de entrenamiento: `train_pima_spark.py`\n"
    "- Este demo usa `@st.cache_resource` para mantener viva la SparkSession."
)
