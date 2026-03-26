# app.py
import streamlit as st
import logging
import os
from datetime import datetime

# --- Configurar carpeta de logs ---
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(
    LOG_DIR,
    f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)

# --- Configurar logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# --- UI Streamlit ---
st.title("Demo logs: INFO, WARNING y ERROR")

st.write(f"Archivo de log actual: `{log_file}`")

if st.button("Registrar INFO"):
    logger.info("Este es un mensaje de INFO desde Streamlit.")
    st.success("INFO registrado en el log.")

if st.button("Registrar WARNING"):
    logger.warning("Este es un mensaje de WARNING desde Streamlit.")
    st.warning("WARNING registrado en el log.")

if st.button("Provocar ERROR"):
    try:
        1 / 0  # Error intencional
    except Exception as e:
        logger.error("Ocurrió un ERROR en la aplicación", exc_info=True)
        st.error("Se provocó un ERROR (revisa el log).")
