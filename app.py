import streamlit as st
import requests

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="Finance Lab | Tomas Tokatlian", layout="wide")

# 2. CSS MAESTRO: ESTILO "MODE" + NAVBAR SUPERIOR SIN PUNTOS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Fraunces:opsz,wght@9,900&display=swap');

    /* Fondo y Colores Base */
    .stApp {
        background-color: #0b1a14;
        color: #e0eadd;
    }

    /* --- NAVBAR SUPERIOR --- */
    .header-container {
        background-color: #f2f7f0;
        padding: 10px 50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        height: 70px;
        border-bottom: 1px solid #e0e6df;
    }

    .logo-text {
        font-family: 'Fraunces', serif;
        font-weight: 900;
        font-size: 1.8rem;
        color: #0b1a14;
    }

    .signature {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 0.7rem;
        color: #0b1a14;
        letter-spacing: 1px;
    }

    /* --- ELIMINAR CÍRCULOS DEL RADIO BUTTON (NAVBAR) --- */
    /* Posicionamiento en el centro de la navbar */
    div[data-testid="stHorizontalRadiogroup"] {
        position: fixed !important;
        top: 18px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 1000 !important;
    }

    /* Escondemos los círculos */
    div[data-testid="stHorizontalRadiogroup"] label div[role="presentation"] {
        display: none !important;
    }

    /* Estilo del texto del menú */
    div[data-testid="stHorizontalRadiogroup"] label div[data-testid="stMarkdownContainer"] p {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        color: #0b1a14 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        margin: 0 !important;
        padding: 5px 15px;
    }

    /* Indicador de selección (Subrayado) */
    div[data-testid="stHorizontalRadiogroup"] label[data-checked="true"] {
        border-bottom: 2px solid #0b1a14 !important;
    }

    /* --- ESTILO DE CONTENIDO --- */
    .main-content { margin-top: 100px; }

    h1 {
        font-family: 'Fraunces', serif !important;
        font-weight: 900 !important;
        color: #c1ff72 !important;
        font-size: 4.5rem !important;
        line-height: 0.9 !important;
        text-align: center;
        margin-bottom: 30px !important;
    }

    /* Dolar Cards (Neón Style) */
    .dolar-card {
        background-color: #122b22;
        border: 1px solid #1a3d31;
        padding: 20px;
        border-radius: 4px;
        transition: all 0.2s ease;
    }
    .dolar-card:hover { border-color: #c1ff72; transform: translateY(-3px); }
    .dolar-nombre { font-family: 'Space Grotesk', sans-serif; color: #8fa391; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; }
    .price-val { font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; font-weight: 700; color: #ffffff; }

    /* Inputs Estilizados */
    .stNumberInput, .stSlider { background-color: #122b22; padding: 10px; border-radius: 4px; border: 1px solid #1a3d31; }

    /* Esconder Sidebar original y basura */
    [data-testid="stSidebar"] { display: none; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER HTML (Logo y Firma)
st.markdown("""
    <div class="header-container">
        <div class="logo-text">FinanceLab</div>
        <div class="signature">TOMAS TOKATLIAN / ANALYST</div>
    </div>
    """, unsafe_allow_html=True)

# 4. SELECTOR DE HERRAMIENTAS (Navbar)
opcion = st.radio(
    "",
    ["Intelligence", "Credit", "Carry"],
    horizontal=True,
    label_visibility="collapsed"
)

# 5. LÓGICA DE DATOS
def obtener_dolares():
    try:
        return requests.get("https://dolarapi.com/v1/dolares").json()
    except:
        return None

# 6. SECCIONES (Contenido restaurado)
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if opcion == "Intelligence":
    st.markdown("<h1>Market<br>Intelligence.</h1>", unsafe_allow_html=True)
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
                                <div><small style="color:#8fa391">COMPRA</small><br><span class="price-val">${d['compra']:.0f}</span></div>
                                <div><small style="color:#8fa391">VENTA</small><br><span class="price-val">${d['venta']:.0f}</span></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            st.write("")
    else:
        st.error("Error cargando API de Dólar.")

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
        st.write("### Análisis de Valor Actual")
        st.markdown(f"<h2 style='color:#c1ff72; font-size:3.5rem;'>PV: ${va_total:,.2f}</h2>", unsafe_allow_html=True)
        if va_total < p_contado:
            st.success(f"Estrategia: Conviene Financiar. Ahorro real: ${p_contado - va_total:,.2f}")
        else:
            st.error("Estrategia: Conviene pagar de Contado.")

elif opcion == "Carry":
    st.markdown("<h1>Arbitrage<br>Strategy.</h1>", unsafe_allow_html=True)
    datos = obtener_dolares()
    blue_vta = 1200.0
    if datos:
        for d in datos:
            if "Blue" in d['nombre']: blue_vta = d['venta']
    
    col1, col2 = st.columns(2)
    with col1:
        usd_cap = st.number_input("Capital Inicial (USD)", value=1000.0)
        tasa_pf = st.number_input("TNA Plazo Fijo (%)", value=40.0)
    with col2:
        dias = st.slider("Plazo (Días)", 30, 180, 30)
        usd_out = st.number_input("Dólar Salida Esperado", value=blue_vta * 1.05)
    
    # Cálculo Carry
    pesos = usd_cap * (blue_vta * 0.98) # Precio compra aprox
    interes = pesos * (tasa_pf/100 * dias / 365)
    usd_fin = (pesos + interes) / usd_out
    ganancia = usd_fin - usd_cap
    
    st.write("---")
    res1, res2 = st.columns(2)
    res1.metric("Resultado Final", f"USD {usd_fin:,.2f}")
    res2.metric("Neto", f"USD {ganancia:,.2f}", delta=f"{(ganancia/usd_cap)*100:.2f}%")

st.markdown('</div>', unsafe_allow_html=True)
