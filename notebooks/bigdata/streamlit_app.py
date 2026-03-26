import streamlit as st
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

# 1) Cachear SparkSession
@st.cache_resource
def get_spark():
    spark = (
        SparkSession.builder
        .appName("pima-streamlit")
        .getOrCreate()
    )
    return spark

# 2) Cachear modelo (sin pasar spark como parámetro)
@st.cache_resource
def get_model():
    model_path = "artefactos/modelo_spark_pima"
    return PipelineModel.load(model_path)

# Instanciar recursos una sola vez
spark = get_spark()
model = get_model()

st.title("🧪 Demo Diabetes (Pima) con Spark + Streamlit")
st.write("Predicción con un modelo entrenado en Apache Spark (Pima.tr MASS).")

npreg = st.slider("Número de embarazos (npreg)", 0, 20, 2)
glu   = st.slider("Nivel de glucosa (glu)", 50, 250, 120)
bp    = st.slider("Presión arterial (bp)", 40, 130, 70)
skin  = st.slider("Espesor del pliegue cutáneo (skin)", 7, 100, 20)
bmi   = st.slider("IMC (bmi)", 10.0, 50.0, 25.0)
ped   = st.slider("Pedigree de diabetes (ped)", 0.0, 2.5, 0.5)
age   = st.slider("Edad (age)", 18, 90, 35)

if st.button("Predecir con Spark"):
    input_df = spark.createDataFrame(
        [(npreg, glu, bp, skin, bmi, ped, age)],
        ["npreg", "glu", "bp", "skin", "bmi", "ped", "age"]
    )

    result = model.transform(input_df).select("probability", "prediction").collect()[0]
    prob = float(result["probability"][1])
    pred = int(result["prediction"])

    etiqueta = "Diabética" if pred == 1 else "No diabética"
    st.write(f"Resultado: **{etiqueta}**")
    st.write(f"Probabilidad de diabetes: **{prob:.2%}**")
