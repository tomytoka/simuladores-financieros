import streamlit as st
import requests

# 1. CONFIGURACIÓN (Debe estar al principio)
st.set_page_config(page_title="Finance Lab", layout="wide")

# 2. LÓGICA DE NAVEGACIÓN (Usando query_params para que parezca una web real)
# Si no hay nada seleccionado, por defecto vamos a 'Intelligence'
if "choice" not in st.session_state:
    st.session_state.choice = "Intelligence"

# Función para cambiar de pestaña
def set_choice(name):
    st.session_state.choice = name

# 3. CSS "MODE" DEFINITIVO (Navbar Real + Estética)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Fraunces:opsz,wght@9,900&display=swap');

    /* Fondo de la App */
    .stApp {{
        background-color: #0b1a14;
    }}

    /* NAVBAR SUPERIOR REAL */
    .nav-wrapper {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 75px;
        background-color: #f2f7f0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 50px;
        z-index: 1000;
        border-bottom: 1px solid #d1d6d0;
    }}

    .logo {{
        font-family: 'Fraunces', serif;
        font-weight: 900;
        font-size: 1.8rem;
        color: #0b1a14;
        flex: 1;
    }}

    .nav-items {{
        display: flex;
        gap: 40px;
        flex: 2;
        justify-content: center;
    }}

    .nav-item {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        color: #0b1a14;
        text-transform: uppercase;
        text-decoration: none;
        cursor: pointer;
        padding-bottom: 5px;
    }}

    .signature-box {{
        flex: 1;
        text-align: right;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.7rem;
        color: #0b1a14;
        letter-spacing: 1px;
    }}

    /* CONTENIDO */
    .main-content {{
        margin-top: 120px;
        text-align: center;
    }}

    h1 {{
        font-family: 'Fraunces', serif !important;
        font-weight: 900 !important;
        color: #c1ff72 !important;
        font-size: 5rem !important;
        line-height: 0.9 !important;
        margin-bottom: 40px !important;
    }}

    /* Cards de Dólares */
    .dolar-card {{
        background-color: #122b22;
        border: 1px solid #1a3d31;
        padding: 25px;
        border-radius: 4px;
        text-align: left;
    }}
    .dolar-card:hover {{ border-color: #c1ff72; }}
    .price-val {{ font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: #ffffff; }}

    /* Ocultar elementos de Streamlit */
    [data-testid="stSidebar"], header, footer, [data-testid="stHeader"] {{
        display: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. DIBUJAR NAVBAR (HTML Puro para que no haya errores de círculos)
# Usamos botones de Streamlit camuflados para la navegación
st.markdown(f"""
    <div class="nav-wrapper">
        <div class="logo">FinanceLab</div>
        <div class="nav-items">
            </div>
        <div class="signature-box">TOMAS TOKATLIAN / ANALYST</div>
    </div>
    """, unsafe_allow_html=True)

# Colocamos los botones de navegación físicamente arriba usando columnas
# Esto reemplaza al radio button problemático
c1, c2, c3, c4, c5, c6, c7 = st.columns([2, 1, 1, 1, 1, 1, 2])
with c3:
    if st.button("Intelligence", key="btn1", use_container_width=True):
        st.session_state.choice = "Intelligence"
with c4:
    if st.button("Credit", key="btn2", use_container_width=True):
        st.session_state.choice = "Credit"
with c5:
    if st.button("Carry", key="btn3", use_container_width=True):
        st.session_state.choice = "Carry"

# CSS Extra para que esos botones parezcan texto de Navbar
st.markdown("""
    <style>
    div.stButton > button {
        background: transparent !important;
        border: none !important;
        color: #0b1a14 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 0.8rem !important;
        margin-top: -120px !important; /* Los subimos a la Navbar */
        position: relative;
        z-index: 1001;
    }
    div.stButton > button:hover {
        color: #c1ff72 !important;
        background: #0b1a14 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 5. LÓGICA DE CONTENIDO
st.markdown('<div class="main-content">', unsafe_allow_html=True)

def obtener_dolares():
    try: return requests.get("https://dolarapi.com/v1/dolares").json()
    except: return None

opcion = st.session_state.choice

if opcion == "Intelligence":
    st.markdown("<h1>Market<br>Intelligence.</h1>", unsafe_allow_html=True)
    datos = obtener_dolares()
    if datos:
        cols = st.columns(3)
        for i, d in enumerate(datos[:6]): # Mostramos los 6 principales
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="dolar-card">
                        <p style="color:#8fa391; font-size:0.7rem; font-family:Space Grotesk;">{d['nombre']}</p>
                        <div style="display:flex; justify-content:space-between;">
                            <div><small style="color:#8fa391">COMPRA</small><br><span class="price-val">${d['compra']:.0f}</span></div>
                            <div><small style="color:#8fa391">VENTA</small><br><span class="price-val">${d['venta']:.0f}</span></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.write("")

elif opcion == "Credit":
    st.markdown("<h1>Unlock<br>Capital.</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    with col1:
        p_contado = st.number_input("Precio Contado ($)", value=100000.0)
        p_cuotas = st.number_input("Precio Cuotas Total ($)", value=125000.0)
        cuotas = st.slider("Cuotas", 1, 24, 12)
        inf = st.slider("Inflación Mensual (%)", 0.0, 15.0, 4.0)
    with col2:
        valor_cuota = p_cuotas / cuotas
        tasa = inf / 100
        va_total = sum([valor_cuota / ((1 + tasa) ** t) for t in range(1, cuotas + 1)])
        st.write("### Análisis de Eficiencia")
        st.markdown
