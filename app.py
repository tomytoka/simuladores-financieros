import streamlit as st
import requests

# 1. CONFIGURACIÓN (Debe estar arriba de todo)
st.set_page_config(page_title="Finance Lab", layout="wide")

# 2. INICIALIZAR ESTADO DE NAVEGACIÓN
if "choice" not in st.session_state:
    st.session_state.choice = "Intelligence"

# 3. TODO EL CSS (Navbar, Botones y Estética Mode)
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

    /* CONTENEDOR DE LOS BOTONES (Fijo arriba de la barra blanca) */
    /* Este bloque fuerza a los botones de Streamlit a quedarse quietos arriba */
    div[data-testid="stHorizontalBlock"] {
        position: fixed !important;
        top: 20px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 1000 !important;
        width: fit-content !important;
    }

    /* ESTILO DE LOS BOTONES PARA QUE PAREZCAN TEXTO */
    div.stButton > button {
        background: transparent !important;
        border: none !important;
        color: #0b1a14 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 0.85rem !important;
        padding: 5px 15px !important;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        color: #c1ff72 !important; /* Verde Neón */
        background-color: #0b1a14 !important;
        border-radius: 4px;
    }

    /* CONTENIDO PRINCIPAL */
    .main-content {
        margin-top: 130px; /* Espacio para que la navbar no tape el título */
    }

    h1 {
        font-family: 'Fraunces', serif !important;
        font-weight: 900 !important;
        color: #c1ff72 !important;
        font-size: 5rem !important;
        line-height: 0.9 !important;
        text-align: center;
        margin-bottom: 40px !important;
    }

    /* Tarjetas de Dólares */
    .dolar-card {
        background-color: #122b22;
        border: 1px solid #1a3d31;
        padding: 25px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    .price-val { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: #ffffff; }

    /* Esconder Sidebar y Headers por defecto */
    [data-testid="stSidebar"], header, footer, [data-testid="stHeader"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. DIBUJAR LA BARRA VISUAL
st.markdown("""
    <div class="nav-bg">
        <div class="logo-text">FinanceLab</div>
        <div class="sig-text">TOMAS TOKATLIAN / ANALYST</div>
    </div>
    """, unsafe_allow_html=True)

# 5. DIBUJAR LOS BOTONES (El CSS los posiciona arriba de la barra blanca)
# Usamos una sola fila de columnas para el menú
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Intelligence", use_container_width=True):
        st.session_state.choice = "Intelligence"
with c2:
    if st.button("Credit", use_container_width=True):
        st.session_state.choice = "Credit"
with c3:
    if st.button("Carry", use_container_width=True):
        st.session_state.choice = "Carry"

# 6. LÓGICA DE CONTENIDO
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
        st.markdown(f"<h2 style='color:#c1ff72; font-size:3.5rem;'>PV: ${va_total:,.2f}</h2>", unsafe_allow_html=True)
        if va_total < p_contado:
            st.success(f"Estrategia: Financiar. Ahorro: ${p_contado - va_total:,.2f}")
        else:
            st.error("Estrategia: Contado.")

elif opcion == "Carry":
    st.markdown("<h1>Arbitrage<br>Strategy.</h1>", unsafe_allow_html=True)
    st.info("Simulador de Carry Trade en desarrollo.")

st.markdown('</div>', unsafe_allow_html=True)
