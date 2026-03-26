import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# 1. Cargar modelo (con caché)
@st.cache_resource
def load_model():
    return joblib.load(Path("artefactos") / "modelo_pima.pkl")

modelo = load_model()

st.title("🤖 Predicción de Diabetes")

# 2. Ingreso de datos del paciente
data = {
    "npreg": st.slider("Número de embarazos", 0, 20, 2),
    "glu":   st.slider("Nivel de glucosa (mg/dl)", 50, 200, 100),
    "bp":    st.slider("Presión arterial (mmHg)", 40, 130, 70),
    "skin":  st.slider("Espesor del pliegue cutáneo (mm)", 7, 100, 20),
    "bmi":   st.slider("IMC", 10.0, 50.0, 25.0),
    "ped":   st.slider("Pedigree de diabetes", 0.0, 2.5, 0.5),
    "age":   st.slider("Edad (años)", 18, 90, 35),
}

# 3. Predicción
if st.button("Predecir"):
    entrada = pd.DataFrame([data])
    prob = modelo.predict_proba(entrada)[0][1]
    pred = int(prob >= 0.5)  # umbral 0.5
    resultado = "Diabética" if pred == 1 else "No diabética"

    st.markdown(f"### Resultado: **{resultado}**")
    st.write(f"Probabilidad estimada de diabetes: **{prob:.2%}**")
    st.caption("Este modelo es solo con fines educativos, no uso clínico.")

# 4. Info en sidebar
st.sidebar.title("ℹ️ Sobre el modelo")
st.sidebar.write(
    "- Dataset: Pima.tr (MASS)\n"
    "- Modelo: LogisticRegression (sklearn)\n"
    "- Entrenamiento: script `train_pima_sklearn.py`\n"
)
