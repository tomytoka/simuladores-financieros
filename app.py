import streamlit as st
import requests

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Finance Lab", layout="wide")

# 2. ESTADO DE NAVEGACIÓN
if "choice" not in st.session_state:
    st.session_state.choice = "Intelligence"

# 3. CSS MAESTRO (Corregido para no romper las columnas de contenido)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Fraunces:opsz,wght@9,900&display=swap');

    /* Fondo de la App */
    .stApp {
        background-color: #0b1a14;
    }

    /* BARRA BLANCA DE FONDO (Fija) */
    .nav-bg {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 80px;
        background-color: #f2f7f0;
        z-index: 998;
        border-bottom: 1px solid #d1d6d0;
        display: flex;
        align-items: center;
        padding: 0 50px;
        justify-content: space-between;
    }

    .logo-text {
        font-family: 'Fraunces', serif;
        font-weight: 900;
        font-size: 1.8rem;
        color: #0b1a14;
    }

    .sig-text {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.7rem;
        color: #0b1a14;
        letter-spacing: 1px;
    }

    /* --- SOLUCIÓN AL ERROR: Solo fijamos el contenedor del MENÚ --- */
    .nav-buttons-container {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        width: 400px; /* Ancho fijo para el menú */
    }

    /* Estilo de los botones del menú */
    div.stButton > button {
        background: transparent !important;
        border: none !important;
        color: #0b1a14 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        color: #c1ff72 !important;
        background-color: #0b1a14 !important;
    }

    /* CONTENIDO PRINCIPAL (Con espacio para la navbar) */
    .main-content {
        margin-top: 150px; /* Bajamos el contenido para que no choque */
    }

    h1 {
        font-family: 'Fraunces', serif !important;
        font-weight: 900 !important;
        color: #c1ff72 !important;
        font-size: 4.5rem !important;
        line-height: 0.9 !important;
        text-align: center;
        margin-bottom: 50px !important;
    }

    /* Tarjetas de Dólares (Ahora sí van a fluir abajo) */
    .dolar-card {
        background-color: #122b22;
        border: 1px solid #1a3d31;
        padding: 25px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    .price-val { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: #ffffff; }

    /* Esconder elementos de Streamlit */
    [data-testid="stSidebar"], header, footer, [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. NAVBAR (HTML + BOTONES)
st.markdown("""
    <div class="nav-bg">
        <div class="logo-text">FinanceLab</div>
        <div class="sig-text">TOMAS TOKATLIAN / ANALYST</div>
    </div>
    """, unsafe_allow_html=True)

# Metemos los botones en un contenedor específico para controlarlos por CSS
st.markdown('<div class="nav-buttons-container">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Intelligence", key="nav1"): st.session_state.choice = "Intelligence"
with c2:
    if st.button("Credit", key="nav2"): st.session_state.choice = "Credit"
with c3:
    if st.button("Carry", key="nav3"): st.session_state.choice = "Carry"
st.markdown('</div>', unsafe_allow_html=True)

# 5. CONTENIDO
st.markdown('<div class="main-content">', unsafe_allow_html=True)

def obtener_dolares():
    try: return requests.get("https://dolarapi.com/v1/dolares").json()
    except: return None

opcion = st.session_state.choice

if opcion == "Intelligence":
    st.markdown("<h1>Market<br>Intelligence.</h1>", unsafe_allow_html=True)
    datos = obtener_dolares()
    if datos:
        cols = st.columns(3) # ESTAS columnas ahora sí van a estar abajo
        for i, d in enumerate(datos[:6]):
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

elif opcion == "Credit":
    st.markdown("<h1>Unlock<br>Capital.</h1>", unsafe_allow_html=True)
    col_input, col_result = st.columns([1, 1.2])
    with col_input:
        p_contado = st.number_input("Precio Contado ($)", value=100000.0)
        p_cuotas = st.number_input("Precio Cuotas Total ($)", value=125000.0)
        cuotas = st.slider("Cuotas", 1, 24, 12)
        inf = st.slider("Inflación Mensual (%)", 0.0, 15.0, 4.0)
    with col_result:
        valor_cuota = p_cuotas / cuotas
        va_total = sum([valor_cuota / ((1 + (inf/100)) ** t) for t in range(1, cuotas + 1)])
        st.write("### Análisis de Eficiencia")
        st.markdown(f"<h2 style='color:#c1ff72; font-size:3.5rem;'>PV: ${va_total:,.2f}</h2>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
