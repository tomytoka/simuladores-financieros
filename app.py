import streamlit as st
import requests

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Finance Lab", layout="wide")

# 2. CSS "MODE" + TOP NAVBAR HACK
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Fraunces:opsz,wght@9,900&display=swap');

    /* Fondo y Base */
    .stApp {
        background-color: #0b1a14;
        color: #e0eadd;
    }

    /* --- NAVBAR HACK --- */
    /* Estilizamos el radio button horizontal para que parezca una Navbar */
    div[role="radiogroup"] {
        justify-content: center;
        background-color: #122b22;
        padding: 10px;
        border-radius: 50px;
        margin: 0 auto 40px auto;
        max-width: fit-content;
        border: 1px solid #1a3d31;
    }
    
    div[role="radiogroup"] > label {
        background-color: transparent !important;
        border: none !important;
        padding: 10px 25px !important;
        color: #8fa391 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 0.8rem;
    }

    div[role="radiogroup"] [data-checked="true"] {
        color: #c1ff72 !important; /* Verde Neón para el activo */
        background-color: #1a3d31 !important;
        border-radius: 40px;
    }

    /* Títulos */
    h1 {
        font-family: 'Fraunces', serif !important;
        font-weight: 900 !important;
        color: #c1ff72 !important;
        line-height: 0.9 !important;
        letter-spacing: -2px !important;
        text-align: center;
    }

    /* Dolar Cards */
    .dolar-card {
        background-color: #122b22;
        border: 1px solid #1a3d31;
        padding: 24px;
        border-radius: 4px;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }
    .dolar-card:hover {
        border-color: #c1ff72;
    }
    .dolar-nombre {
        font-family: 'Space Grotesk', sans-serif;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 2px;
        color: #8fa391;
        font-size: 0.7rem;
    }
    .price-grid {
        display: flex;
        justify-content: space-between;
        margin-top: 15px;
    }
    .price-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
    }
    .price-label { font-size: 0.6rem; color: #8fa391; display: block; }

    /* Ocultar Sidebar y Basura */
    [data-testid="stSidebar"] { display: none; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE DATOS
def obtener_dolares():
    try:
        return requests.get("https://dolarapi.com/v1/dolares").json()
    except:
        return None

# 4. TOP NAVBAR (En lugar de Sidebar)
# Usamos un st.radio horizontal como nuestra Navbar
opcion = st.radio(
    "",
    ["Market Intelligence", "Credit Analysis", "Carry Strategy"],
    horizontal=True,
    label_visibility="collapsed"
)

# Datos
datos_dolar = obtener_dolares()

# 5. SECCIONES
if opcion == "Market Intelligence":
    st.markdown("<h1>Market<br>Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#8fa391;'>Real-time monetary data visualization.</p>", unsafe_allow_html=True)
    st.write("##")

    if datos_dolar:
        for i in range(0, len(datos_dolar), 3):
            cols = st.columns(3)
            grupo = datos_dolar[i:i+3]
            for j, d in enumerate(grupo):
                with cols[j]:
                    st.markdown(f"""
                        <div class="dolar-card">
                            <div class="dolar-nombre">{d['nombre']}</div>
                            <div class="price-grid">
                                <div class="price-box">
                                    <span class="price-label">COMPRA</span>
                                    <span class="price-value">${d['compra']:.0f}</span>
                                </div>
                                <div class="price-box">
                                    <span class="price-label">VENTA</span>
                                    <span class="price-value">${d['venta']:.0f}</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.error("API error.")

elif opcion == "Credit Analysis":
    st.markdown("<h1>Unlock<br>Capital.</h1>", unsafe_allow_html=True)
    st.write("##")
    
    col1, col2 = st.columns([1, 1.2])
    with col1:
        p_contado = st.number_input("Cash Price ($)", value=100000.0)
        p_cuotas = st.number_input("Installment Total ($)", value=125000.0)
        cuotas = st.slider("Installments", 1, 24, 12)
        inf = st.slider("Exp. Monthly Inflation (%)", 0.0, 15.0, 4.0)
    
    with col2:
        valor_cuota = p_cuotas / cuotas
        tasa = inf / 100
        va_total = sum([valor_cuota / ((1 + tasa) ** t) for t in range(1, cuotas + 1)])
        ahorro = p_contado - va_total
        
        st.write("### Analysis")
        st.markdown(f"<h2 style='text-align:left; font-size:3rem;'>PV: ${va_total:,.2f}</h2>", unsafe_allow_html=True)
        
        if va_total < p_contado:
            st.success(f"Strategy: Efficient Financing. Saving: ${ahorro:,.2f}")
        else:
            st.error("Strategy: Cash Optimal.")

elif opcion == "Carry Strategy":
    st.markdown("<h1>Arbitrage<br>Model.</h1>", unsafe_allow_html=True)
    # Aquí podrías completar con el código de Carry Trade anterior
    st.write("---")
    st.markdown("<p style='text-align:center;'>Section under development.</p>", unsafe_allow_html=True)

# Footer con tu nombre (como es una sola página, lo ponemos abajo)
st.write("##")
st.markdown(f"<p style='text-align:center; color:#c1ff72; font-family:Space Grotesk; font-size:0.8rem; letter-spacing:2px;'>DEVELOPED BY TOMAS TOKATLIAN / FINANCES</p>", unsafe_allow_html=True)
