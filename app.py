import streamlit as st
import requests

# 1. CONFIGURACIÓN (Solo una vez y al principio)
st.set_page_config(
    page_title="Finance Lab | Portfolio", 
    page_icon="📈", 
    layout="wide"
)

# 2. ESTILO CSS "EDITORIAL DASHBOARD"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;600&display=swap');

    html, body, [class*="css"], .stText {
        font-family: 'Inter', sans-serif;
        color: #e5e5e5;
    }

    .stApp {
        background-color: #1a1614;
        background-image: radial-gradient(circle at 10% 10%, rgba(255, 107, 53, 0.05) 0%, transparent 50%),
                          radial-gradient(circle at 90% 90%, rgba(255, 107, 53, 0.02) 0%, transparent 50%);
    }

    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 4rem !important;
        font-weight: 900 !important;
        color: #ff6b35 !important;
        line-height: 1.1 !important;
        margin-bottom: 10px !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.02);
        border: none;
        border-left: 3px solid #ff6b35;
        padding: 30px !important;
        border-radius: 0px;
        transition: all 0.4s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        background: rgba(255, 107, 53, 0.08);
        transform: translateX(5px);
    }

    [data-testid="stMetricLabel"] p {
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 0.75rem !important;
        color: #888 !important;
    }

    [data-testid="stMetricValue"] div {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.8rem !important;
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. FUNCIONES
def obtener_dolares():
    try:
        url = "https://dolarapi.com/v1/dolares"
        res = requests.get(url)
        return res.json()
    except:
        return None

# 4. LÓGICA DE NAVEGACIÓN
st.sidebar.markdown("<h2 style='color:#ff6b35;'>Navegación</h2>", unsafe_allow_html=True)
opcion = st.sidebar.selectbox(
    "Seleccione una herramienta:",
    ["Mercado de Cambios", "Análisis de Financiación", "Estrategia Carry Trade"]
)

st.sidebar.divider()
st.sidebar.markdown("### **Tomas Tokatlian**")
st.sidebar.caption("Financial Analysis & Development")

datos_dolar = obtener_dolares()

# 5. SECCIONES
if opcion == "Mercado de Cambios":
    st.markdown("<h1 class='hero-title'>Turning data <br>into value.</h1>", unsafe_allow_html=True)
    st.write("---")
    
    if datos_dolar:
        for i in range(0, len(datos_dolar), 3):
            cols = st.columns(3)
            grupo = datos_dolar[i:i+3]
            for j, d in enumerate(grupo):
                with cols[j]:
                    st.metric(
                        label=d['nombre'], 
                        value=f"${d['venta']:,.0f}", 
                        delta=f"Compra: ${d['compra']:,.0f}"
                    )
            st.write("") 
    else:
        st.error("Error al cargar cotizaciones.")

elif opcion == "Análisis de Financiación":
    st.markdown("<h1 class='hero-title'>Credit vs. Cash</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.5])
    with col1:
        p_contado = st.number_input("Precio de Contado ($)", value=100000.0)
        p_cuotas = st.number_input("Precio Total Financiado ($)", value=125000.0)
        cuotas = st.slider("Cantidad de cuotas", 1, 24, 12)
        inf = st.slider("Inflación mensual (%)", 0.0, 15.0, 4.0)
    
    with col2:
        valor_cuota = p_cuotas / cuotas
        tasa = inf / 100
        va_total = sum([valor_cuota / ((1 + tasa) ** t) for t in range(1, cuotas + 1)])
        st.metric("Costo Real (Valor de Hoy)", f"${va_total:,.2f}")
        if va_total < p_contado:
            st.success("Conviene financiar.")
        else:
            st.error("Conviene pagar al contado.")

elif opcion == "Estrategia Carry Trade":
    st.markdown("<h1 class='hero-title'>Carry Trade <br>Strategy.</h1>", unsafe_allow_html=True)
    blue_price = 1200.0
    if datos_dolar:
        for d in datos_dolar:
            if "Blue" in d['nombre']: blue_price = d['venta']

    col1, col2 = st.columns(2)
    with col1:
        usd_vender = st.number_input("Capital (USD)", value=1000.0)
        tasa_pf = st.number_input("TNA Plazo Fijo (%)", value=40.0)
    with col2:
        plazo_dias = st.slider("Plazo (Días)", 30, 180, 30)
        usd_futuro = st.number_input("Precio dólar salida", value=blue_price * 1.05)

    pesos = usd_vender * (blue_price * 0.98)
    total_pesos = pesos + (pesos * (tasa_pf/100 * plazo_dias / 365))
    usd_finales = total_pesos / usd_futuro
    ganancia = usd_finales - usd_vender
    
    st.metric("Resultado Neto", f"USD {usd_finales:,.2f}", delta=f"{ganancia:,.2f} USD")
