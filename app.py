import streamlit as st
import requests

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Finance Lab", layout="wide")

# 2. CSS AGRESIVO: NAVBAR "MODE" DEFINITIVA
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Fraunces:opsz,wght@9,900&display=swap');

    /* --- RESET Y COLORES BASE --- */
    .stApp {
        background-color: #0b1a14; /* Fondo oscuro Mode */
    }

    /* --- CONTENEDOR DE LA NAVBAR (Fija arriba) --- */
    .header-container {
        background-color: #f2f7f0; /* Fondo crema de la foto */
        padding: 10px 50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        border-bottom: 1px solid #e0e6df;
        height: 70px;
    }

    /* --- LOGO A LA IZQUIERDA --- */
    .logo-text {
        font-family: 'Fraunces', serif;
        font-weight: 900;
        font-size: 1.8rem;
        color: #0b1a14;
        text-decoration: none;
        flex: 1; /* Ocupa espacio a la izquierda */
    }

    /* --- TU FIRMA A LA DERECHA (Refinada) --- */
    .tomas-signature {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.75rem;
        color: #0b1a14;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: right;
        flex: 1; /* Ocupa espacio a la derecha */
    }

    /* --- CONTENIDO PRINCIPAL (Abajo de la Navbar) --- */
    .main-content {
        margin-top: 100px;
    }

    /* --- ESTILO DE TÍTULOS GRANDES --- */
    h1 {
        font-family: 'Fraunces', serif !important;
        font-weight: 900 !important;
        color: #c1ff72 !important;
        font-size: 5rem !important;
        line-height: 0.9 !important;
        text-align: center;
    }

    /* --- HACK CRÍTICO DEL MENÚ (st.radio) --- */
    /* 1. Posicionamos el menú en el CENTRO absoluto de la navbar */
    div[data-testid="stHorizontalRadiogroup"] {
        position: fixed !important;
        top: 15px !important; /* Ajuste fino vertical */
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 1000;
        background-color: transparent !important;
        gap: 25px !important;
    }
    
    /* 2. OCULTAMOS LOS PUNTITOS (Círculos de selección) */
    div[data-testid="stHorizontalRadiogroup"] label div[role="presentation"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
    }

    /* 3. HACEMOS QUE APAREZCAN LOS NOMBRES DE LAS HERRAMIENTAS */
    div[data-testid="stHorizontalRadiogroup"] label div[data-testid="stMarkdownContainer"] p {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        color: #0b1a14 !important; /* Texto oscuro sobre la navbar clara */
        text-transform: capitalize;
        text-align: center;
        margin: 0 !important;
    }

    /* 4. Estilo de subrayado para el ítem seleccionado */
    div[data-testid="stHorizontalRadiogroup"] label[data-checked="true"] {
        background-color: transparent !important;
        border-bottom: 2px solid #0b1a14 !important;
        padding-bottom: 2px;
    }

    /* Ocultar elementos molestos de Streamlit */
    [data-testid="stSidebar"] { display: none; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. ESTRUCTURA DE LA NAVBAR (HTML Estático para Logo y Firma)
st.markdown(f"""
    <div class="header-container">
        <div class="logo-text">Mode</div>
        <div class="tomas-signature">DEVELOPED BY TOMAS TOKATLIAN</div>
    </div>
    """, unsafe_allow_html=True)

# 4. MENÚ DE NAVEGACIÓN (st.radio horizontal)
# El CSS se encarga de centrarlo y estilizarlo como Navbar
opcion = st.radio(
    "",
    ["Market Intelligence", "Credit Analysis", "Carry Strategy"],
    horizontal=True,
    label_visibility="collapsed"
)

# 5. CONTENIDO DE LAS SECCIONES
st.markdown('<div class="main-content">', unsafe_allow_html=True)

def obtener_dolares():
    try: return requests.get("https://dolarapi.com/v1/dolares").json()
    except: return None

if opcion == "Market Intelligence":
    st.markdown("<h1>Intelligence <br>built around <br>markets.</h1>", unsafe_allow_html=True)
    st.write("##")
    # Lógica de dólares aquí...

elif opcion == "Credit Analysis":
    st.markdown("<h1>Unlock <br>Efficient <br>Capital.</h1>", unsafe_allow_html=True)
    # Lógica de crédito aquí...

st.markdown('</div>', unsafe_allow_html=True)
