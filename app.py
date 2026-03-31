import streamlit as st
import requests

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero)
st.set_page_config(
    page_title="Finance Lab | Portfolio", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTILO CSS "EDITORIAL DASHBOARD" (Inspirado en Ventriloc)
st.markdown("""
    <style>
    /* Importar fuentes de alta gama */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;600&display=swap');

    /* Reset General y Tipografía */
    html, body, [class*="css"], .stText {
        font-family: 'Inter', sans-serif;
        color: #e5e5e5;
    }

    /* Fondo de la aplicación: Charcoal Deep */
    .stApp {
        background-color: #1a1614;
        background-image: radial-gradient(circle at 10% 10%, rgba(255, 107, 53, 0.05) 0%, transparent 50%),
                          radial-gradient(circle at 90% 90%, rgba(255, 107, 53, 0.02) 0%, transparent 50%);
    }

    /* Estilo de los Títulos (Serif) */
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 4.5rem !important;
        font-weight: 900 !important;
        color: #ff6b35 !important; /* Naranja Editorial */
        line-height: 1.1 !important;
        margin-bottom: 10px !important;
    }

    h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #f5f5f5 !important;
    }

    /* Tarjetas de Datos (Métricas) */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.02);
        border: none;
        border-left: 3px solid #ff6b35; /* Acento lateral */
        padding: 30px !important;
        border-radius: 0px;
        transition: all 0.4s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        background: rgba(255, 107, 53, 0.08);
        transform: translateX(5px);
    }

    /* Estética de Números y Etiquetas */
    [data-testid="stMetricLabel"] p {
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 0.75rem !important;
