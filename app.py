import streamlit as st
import requests

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Finance Lab", layout="wide")

# 2. CSS ESTILO "MODE" (Verde Neón + Retro-Moderno)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Fraunces:opsz,wght@9,900&display=swap');

    /* Fondo verde muy oscuro (Mode style) */
    .stApp {
        background-color: #0b1a14;
        color: #e0eadd;
    }

    /* Tipografía de Títulos (Fraunces - Retro Serif) */
    h1, h2 {
        font-family: 'Fraunces', serif !important;
        font-weight: 900 !important;
        color: #c1ff72 !important; /* Verde Neón */
        line-height: 0.9 !important;
        letter-spacing: -2px !important;
    }

    /* Contenedores de Dólares */
    .dolar-card {
        background-color: #122b22;
        border: 2px solid #1a3d31;
        padding: 24px;
        border-radius: 4px; /* Bordes más cuadrados (Retro) */
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }

    .dolar-card:hover {
        border-color: #c1ff72;
        transform: scale(1.02);
    }

    .dolar-nombre {
        font-family: 'Space Grotesk', sans-serif;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 2px;
        color: #8fa391;
        font-size: 0.8rem;
    }

    .price-grid {
        display: flex;
        justify-content: space-between;
        margin-top: 15px;
    }

    .price-box {
        flex: 1;
    }

    .price-label {
        font-size: 0.7rem;
        color: #8fa391;
        display: block;
    }

    .price-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
    }

    /* Estilo de Inputs y Sliders */
    .stNumberInput, .stSlider {
        background-color: #122b22;
        padding: 15px;
        border-radius: 4px;
    }

    /* Ocultar basura de Streamlit */
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE DATOS
def obtener_dolares():
    try:
        url = "https://dolarapi.com/v1/dolares"
        return requests.get(url).json()
    except:
        return None

# 4. NAVEGACIÓN (Sidebar)
st.sidebar.markdown("<h1 style='font-size: 2rem;'>Lab.</h1>", unsafe_allow_html=True)
opcion = st.sidebar.selectbox("Herramientas", ["Cotizaciones", "Credit Analysis", "Carry Strategy"])
st.sidebar.write("---")
st.sidebar.markdown(f"<p style='color:#c1ff72'>Tomas Tokatlian</p>", unsafe_allow_html=True)

datos_dolar = obtener_dolares()

# 5. SECCIONES
if opcion == "Cotizaciones":
    st.markdown("<h1 style='font-size: 5rem;'>Market<br>Intelligence</h1>", unsafe_allow_html=True)
    st.write("##")

    if datos_dolar:
        # Mostramos los dólares en una grilla personalizada (No usamos st.metric para evitar el error)
        for i in range(0, len(datos_dolar), 3):
            cols = st.columns(3)
            grupo = datos_dolar[i:i+3]
            for j, d in enumerate(grupo):
                with cols[j]:
                    # Creamos nuestra propia tarjeta con HTML para control total
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
        st.error("Data provider offline.")

elif opcion == "Credit Analysis":
    st.markdown("<h1 style='font-size: 4rem;'>Unlock<br>Capital.</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2])
    with col1:
        p_contado = st.number_input("Cash Price ($)", value=100000.0)
        p_cuotas = st.number_input("Installment Total ($)", value=125000.0)
        cuotas = st.slider("Installments", 1, 24, 12)
        inf = st.slider("Exp. Inflation (%)", 0.0, 15.0, 4.0)
    
    with col2:
        valor_cuota = p_cuotas / cuotas
        tasa = inf / 100
        va_total = sum([valor_cuota / ((1 + tasa) ** t) for t in range(1, cuotas + 1)])
        ahorro = p_contado - va_total
        
        st.write("### Analysis Result")
        st.markdown(f"<h2 style='font-size: 3rem;'>PV: ${va_total:,.2f}</h2>", unsafe_allow_html=True)
        
        if va_total < p_contado:
            st.success(f"Strategy: Financing is efficient. Real saving: ${ahorro:,.2f}")
        else:
            st.error("Strategy: Cash payment is optimal.")

elif opcion == "Carry Strategy":
    st.markdown("<h1 style='font-size: 4rem;'>Arbitrage<br>Model.</h1>", unsafe_allow_html=True)
    # Lógica de Carry Trade simplificada aquí...
    st.write("Dashboard interactivo en desarrollo bajo estética 'Mode'.")
