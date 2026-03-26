# ============================================================
# Imagen docker M2M (del aprendizaje Manual al Automático)
# Docker → Jupyter → Entrenamiento → Artefactos (joblib) → Deploy (demo)
# ============================================================

# Imagen base ligera con conda + mamba y canal conda-forge
FROM condaforge/miniforge3:latest

# Usamos bash como shell por defecto y activamos pipefail
# para que falle el comando completo si alguno en un pipe falla
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# pip no guarda caché → imagen más ligera
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 

# Carpeta de trabajo
RUN mkdir -p /opt/notebooks
WORKDIR /opt/notebooks

# ------------------------------------------------------------
# Núcleo científico ML (conda-forge) + Jupyter
#   - Python 3.11
#   - Stack típico de ciencia de datos (numpy/pandas/sklearn, etc.)
#   - Jupyter Notebook + JupyterLab incluidos
#   - tini: init ligero para manejar correctamente señales/child procs
# ------------------------------------------------------------
RUN mamba install -y python=3.11 notebook=7.2 jupyterlab=4.2 ipykernel \
      numpy=1.26 pandas=2.2 scikit-learn=1.5 imbalanced-learn=0.12 \
      joblib=1.4 statsmodels=0.14 catboost=1.2 matplotlib=3.8 seaborn=0.13 \
      tini && conda clean -afy

# -------------------------------------------------------
# Streamlit (PARA DEPLOY)
# -------------------------------------------------------
RUN pip install --upgrade streamlit

# ==============================
# OPCIONAL 
# ==============================

# -------------------------------------------------------
# Apache Spark (OPCIONAL)
#   Descomenta TODO este bloque si quieres usar Spark
#   1) Java (openjdk 17)
#   2) PySpark + Arrow + findspark
# -------------------------------------------------------
RUN mamba install -y openjdk=17 && conda clean -afy
ENV JAVA_HOME=/opt/conda
ENV PATH="$JAVA_HOME/bin:$PATH"
RUN pip install pyspark==3.5.1 pyarrow==14.0.2 findspark
EXPOSE 4040

# -------------------------------------------------------
# Java (kernel Java para Jupyter) — OPCIONAL
#   Requiere Java (openjdk=17), que ya instalas para Spark
#   Descomenta si quieres un kernel "Java" en Jupyter
# -------------------------------------------------------
# RUN mamba install -y scijava-jupyter-kernel && conda clean -afy

# -------------------------------------------------------
# R (IRkernel)  — OPCIONAL
#   Descomenta este bloque si quieres un kernel "R" en Jupyter
# -------------------------------------------------------
# RUN mamba install -y r-base r-irkernel && \
#     R -e "IRkernel::installspec(user = FALSE)" && \
#     conda clean -afy

# -------------------------------------------------------
# C++ (xeus-cling) — OPCIONAL
#   Descomenta si quieres kernels C++11/C++14 en Jupyter
# -------------------------------------------------------
# RUN mamba install -y xeus-cling && conda clean -afy

# -------------------------------------------------------
# Exportar a PDF vía WebPDF (OPCIONAL - Chromium)
#   Descomenta SOLO si necesitas PDF
# -------------------------------------------------------
# RUN pip install -U "nbconvert[webpdf]" playwright && \
#     playwright install --with-deps chromium

# -------------------------------------------------------
# Exportar a PDF vía LaTeX (OPCIONAL - ELEGANTE PERO MUY PESADO)
# -------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
     pandoc \
     texlive-xetex \
     texlive-fonts-recommended \
     texlive-latex-recommended \
     texlive-latex-extra \
     texlive-plain-generic \
     build-essential g++ curl unzip && \
     apt-get clean && rm -rf /var/lib/apt/lists/*
# ==============================

# Dependencias del proyecto (OPCIONAL FIN)
ADD requirements.txt /requirements.txt
RUN pip install --no-deps -r /requirements.txt

# Puerto para Jupyter y Streamlit
EXPOSE 3131 8501

ENTRYPOINT ["tini", "--"]

CMD ["jupyter", "notebook", "--notebook-dir=/opt/notebooks", "--ip=0.0.0.0", "--port=3131", "--no-browser", "--allow-root"]