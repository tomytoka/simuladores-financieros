import streamlit as st
import requests

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Finance Lab | Mode Style", layout="wide")

# 2. CSS AVANZADO: NAVBAR "MODE" Y ESTRUCTURA PROFESIONAL
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Fraunces:opsz,wght@9,900&display=swap');

    /* --- RESET Y COLORES BASE --- */
    .stApp {
        background-color: #0b1a14; /* Fondo oscuro Mode */
    }

    /* --- NAVBAR SUPERIOR --- */
    /* Contenedor principal de la Navbar */
    .header-container {
        background-color: #f2f7f0; /* Fondo crema de la foto */
        padding: 15px 50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        border-bottom: 1px solid #e0e6df;
    }

    /* Estilo del "Logo" */
    .logo-text {
        font-family: 'Fraunces', serif;
        font-weight: 900;
        font-size: 1.8rem;
        color: #0b1a14;
        text-decoration: none;
    }

    /* --- HACK DEL MENÚ DE NAVEGACIÓN --- */
    /* Estilizamos el radio button horizontal para que parezca un menú de texto plano */
    div[role="radiogroup"] {
        background-color: transparent !important;
        border: none !important;
        gap: 20px !important;
    }
    
    /* Escondemos los círculos de selección */
    div[role="radiogroup"] [data-testid="stWidgetLabel"] { display: none; }
    div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        color: #0b1a14 !important;
        text-transform: capitalize;
    }

    /* Estilo del ítem seleccionado (subrayado sutil) */
    div[role="radiogroup"] [data-checked="true"] {
        background-color: transparent !important;
        border-bottom: 2px solid #0b1a14 !important;
    }
    
    /* Quitamos el círculo visual */
    div[role="radiogroup"] label div[role="presentation"] {
        display: none !important;
    }

    /* --- BOTONES DERECHA --- */
    .nav-buttons {
        display: flex;
        gap: 15px;
    }
    .btn-outline {
        padding: 8px 18px;
        border: 1.5px solid #0b1a14;
        border-radius: 5px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.8rem;
        color: #0b1a14;
    }
    .btn-solid {
        padding: 8px 18px;
        background-color: #0b1a14;
        border-radius: 5px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.8rem;
        color: #f2f7f0;
    }

    /* --- CONTENIDO --- */
    .main-content {
        margin-top: 100px; /* Para que no lo tape la navbar */
    }

    h1 {
        font-family: 'Fraunces', serif !important;
        font-weight: 900 !important;
        color: #c1ff72 !important;
        font-size: 5rem !important;
        line-height: 0.9 !important;
        text-align: center;
    }

    /* Dolar Cards */
    .dolar-card {
        background-color: #122b22;
        border: 1px solid #1a3d31;
        padding: 24px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    .dolar-nombre { font-family: 'Space Grotesk', sans-serif; color: #8fa391; font-size: 0.7rem; letter-spacing: 1px;}
    .price-value { font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; font-weight: 700; color: #ffffff; }

    /* Ocultar elementos genéricos */
    [data-testid="stSidebar"] { display: none; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. ESTRUCTURA DE LA NAVBAR (HTML)
st.markdown(f"""
    <div class="header-container">
        <div class="logo-text">Mode</div>
        <div id="nav-placeholder"></div> <div class="nav-buttons">
            <div class="btn-outline">Sign in</div>
            <div class="btn-solid">Try for free</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. MENÚ DE NAVEGACIÓN (Radio horizontal)
# Lo centramos con columnas para que quede en el medio de la navbar
_, col_nav, _ = st.columns([1, 2, 1])
with col_nav:
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
    st.markdown("<h1>Business Intelligence <br>built around <br>markets.</h1>", unsafe_allow_html=True)
    st.write("##")
    
    datos = obtener_dolares()
    if datos:
        for i in range(0, len(datos), 3):
            cols = st.columns(3)
            grupo = datos[i:i+3]
            for j, d in enumerate(grupo):
                with cols[j]:
                    st.markdown(f"""
                        <div class="dolar-card">
                            <div class="dolar-nombre">{d['nombre']}</div>
                            <div style="display:flex; justify-content:space-between; margin-top:10px;">
                                <div><small style="color:#8fa391">COMPRA</small><br><span class="price-value">${d['compra']:.0f}</span></div>
                                <div><small style="color:#8fa391">VENTA</small><br><span class="price-value">${d['venta']:.0f}</span></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

elif opcion == "Credit Analysis":
    st.markdown("<h1>Unlock <br>Efficient <br>Capital.</h1>", unsafe_allow_html=True)
    # Lógica de crédito aquí...

st.markdown('</div>', unsafe_allow_html=True)
