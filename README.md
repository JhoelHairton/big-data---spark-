# 🚀 Entorno M2M (del aprendizaje **Manual** al **Automático**) con Docker

**Jupyter Notebook/Lab** es todo lo que necesitas.  
Lleva tus proyectos de *machine learning* a otro nivel y, cuando quieras, habilita/comenta **Streamlit**, **Spark**, **R**, **Java** o **C++**.

---

## ✨ ¿Qué incluye este entorno?

Por defecto (sin tocar nada) tienes:

- Python 3.11 (vía `conda-forge` / Miniforge).
- Stack mínimo de **ML clásico**:
  - `numpy`, `pandas`, `scikit-learn`, `imbalanced-learn`, `statsmodels`, `catboost`, `joblib`.
- JupyterLab listo en Docker.
- Carpeta `notebooks/` mapeada desde tu host.

Todo lo demás (**Streamlit, Spark, R, Java, C++**) se activa **solo comentando/descomentando** bloques en el `Dockerfile` y el `docker-compose.yaml`.

---

## 🧱 Archivos principales

- `Dockerfile`  
  Define la imagen base con:
  - Núcleo de ML (obligatorio).
  - Bloques **opcionales** para:
    - Streamlit  
    - Spark (Big Data)  
    - R (IRkernel)  
    - Java (kernel IJava)  
    - C++ (xeus-cling)

- `docker-compose.yaml`  
  Levanta el servicio `m2m` con:
  - Puertos mapeados (Jupyter, y opcionales Streamlit / Spark UI).
  - Volumen `./notebooks:/opt/notebooks`.

---

## 🧩 Modos de trabajo

### 1️⃣ Modo ML básico (por defecto)

Ideal para el grupo que solo verá **modelos de ML clásico**:

- No toques el `Dockerfile` (usa solo el bloque de núcleo ML).
- Deja comentados todos los bloques opcionales.
- No abras puertos extra en `docker-compose.yaml`.

Tendrás:

- JupyterLab en `http://localhost:3131`
- Bibliotecas de ML clásico listas para usar.

---

### 2️⃣ Modo ML + Streamlit (apps interactivas)

Para el grupo que hará **dashboards / demos** con Streamlit:

1. En el `Dockerfile`, descomenta:

   ```dockerfile
   # --- Streamlit (OPCIONAL) ---
   RUN pip install --no-cache-dir --upgrade streamlit
   EXPOSE 8501
"# big-data---spark-" 
