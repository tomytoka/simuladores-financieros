import streamlit as st
import requests

# 1. Configuración de página
st.set_page_config(page_title="Finance Lab", layout="wide")

# 2. CSS "THE FORCE": Forzamos a Streamlit a verse como Mode
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Fraunces:opsz,wght@9,900&display=swap');

    /* Fondo de la App */
    .stApp {
        background-color: #0b1a14;
    }

    /* NAVBAR FIJA SUPERIOR */
    .header-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 80px;
        background-color: #f2f7f0; /* El color crema de Mode */
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 50px;
        z-index: 99;
        border-bottom: 1px solid #d1d6d0;
    }

    .logo {
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

    /* POSICIONAR EL MENÚ DENTRO DE LA NAVBAR */
    div[data-testid="stHorizontalRadiogroup"] {
        position: fixed !important;
        top: 25px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 100 !important;
        background-color: transparent !important;
        gap: 30px !important;
    }

    /* OCULTAR LOS CÍRCULOS (EL HACK DEFINITIVO) */
    /* Este selector busca específicamente el círculo y lo elimina */
    div[data-testid="stHorizontalRadiogroup"] label div[role="presentation"] {
        display: none !important;
    }
    
    /* Estilo de los textos del menú */
    div[data-testid="stHorizontalRadiogroup"] label div[data-testid="stMarkdownContainer"] p {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        color: #0b1a14 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        margin: 0 !important;
        cursor: pointer;
    }

    /* Indicador de selección (Subrayado negro) */
    div[data-testid="stHorizontalRadiogroup"] label[data-checked="true"] {
        border-bottom: 2px solid #0b1a14 !important;
        padding-bottom: 5px !important;
    }

    /* CONTENIDO PRINCIPAL */
    .main-content {
        margin-top: 130px;
        padding: 0 20px;
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

    /* Dolar Cards */
    .dolar-card {
        background-color: #122b22;
        border: 1px solid #1a3d31;
        padding: 25px;
        border-radius: 4px;
        transition: all 0.2s ease;
    }
    .dolar-card:hover { border-color: #c1ff72; transform: translateY(-3px); }
    .dolar-nombre { font-family: 'Space Grotesk', sans-serif; color: #8fa391; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; }
    .price-val { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: #ffffff; }

    /* Estilo de inputs */
    .stNumberInput, .stSlider { 
        background-color: #122b22 !important; 
        border: 1px solid #1a3d31 !important; 
        border-radius: 4px !important; 
    }

    /* Esconder Sidebar y Header de Streamlit */
    [data-testid="stSidebar"] { display: none; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header HTML Estático
st.markdown("""
    <div class="header-container">
        <div class="logo">FinanceLab</div>
        <div class="signature">TOMAS TOKATLIAN / ANALYST</div>
    </div>
    """, unsafe_allow_html=True)

# 4. El Radio (Navegación)
# El CSS lo va a mover mágicamente adentro de la barra blanca
opcion = st.radio(
    "",
    ["Intelligence", "Credit", "Carry"],
    horizontal=True,
    label_visibility="collapsed"
)

# 5. Lógica de Datos
def obtener_dolares():
    try:
        return requests.get("https://dolarapi.com/v1/dolares").json()
    except:
        return None

# 6. Renderizado de Contenido
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
    else:
        st.error("Error cargando datos.")

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
    st.info("Simulador de Carry Trade activo.")
    # (Aquí podés pegar la lógica de Carry que ya tenías)

st.markdown('</div>', unsafe_allow_html=True)
