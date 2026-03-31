import streamlit as st
import requests

# Configuración de página (Ponele layout="wide" para usar todo el espacio)
st.set_page_config(page_title="My Finance Lab", page_icon="📊", layout="wide")

# --- CSS AVANZADO: Fondo con Gradientes y Tarjetas Modernas ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* 1. Reset General */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* 2. Fondo: Más oscuro y elegante */
    .stApp {
        background: #050505;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(0, 168, 232, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(50, 255, 126, 0.05) 0%, transparent 40%);
    }

    /* 3. Títulos Gradientes */
    h1 {
        font-weight: 800 !important;
        background: linear-gradient(90deg, #FFFFFF, #888888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }

    /* 4. TARJETAS (Métricas) - Look Pro */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px !important;
        border-radius: 20px;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(50, 255, 126, 0.3);
        transform: translateY(-5px);
    }

    /* 5. Ajuste de textos en métricas */
    label[data-testid="stMetricLabel"] p {
        font-size: 0.9rem !important;
        color: #888888 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div[data-testid="stMetricValue"] div {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #32ff7e !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Configuración de página (NOMBRE DE TU PROYECTO)
st.set_page_config(page_title="Herramientas Finanieras", page_icon="📊", layout="wide")

# Estilo personalizado para las tarjetas (CSS)
st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: #1e212b;
        border: 1px solid #323641;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    stMetric label {
        color: #8a8d97 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Herramientas Financieras")
st.write("Herramientas interactivas para análisis financiero y toma de decisiones.")

# --- FUNCIÓN PARA OBTENER DÓLAR ---
if opcion == "Cotizaciones en Tiempo Real":
    st.markdown("# Mercado de Cambios")
    st.caption("Precios de referencia para la toma de decisiones financieras.")
    st.write("---") # Una línea divisoria fina

    if datos_dolar:
        # Usamos contenedores para agrupar
        with st.container():
            for i in range(0, len(datos_dolar), 3):
                cols = st.columns(3)
                grupo = datos_dolar[i:i+3]
                for j, d in enumerate(grupo):
                    with cols[j]:
                        st.metric(
                            label=d['nombre'], 
                            value=f"${d['venta']:,.0f}", 
                            delta=f"Compra: ${d['compra']:,.0f}",
                            delta_color="normal"
                        )
                st.write("") # Espacio entre filas
    else:
        st.error("Error al conectar con la API.")

# --- MENÚ LATERAL ---
st.sidebar.title("Navegación")
opcion = st.sidebar.selectbox("Elegí un simulador", 
    ["Cotizaciones en Tiempo Real", "Cuotas vs Contado", "Carry Trade (Bicicleta)"])
st.sidebar.divider()
st.sidebar.markdown("### **Desarrollado por Tomas Tokatlian**")
st.sidebar.write("Estudiante de Lic. en Finanzas")
datos_dolar = obtener_dolares()

# --- SECCIÓN 1: COTIZACIONES ---
if opcion == "Cotizaciones en Tiempo Real":
    st.header("💵 Cotizaciones Actuales (Argentina)")
    st.write("Datos en tiempo real extraídos de DolarApi.")

    if datos_dolar:
        # Creamos una grilla de 3 columnas
        for i in range(0, len(datos_dolar), 3):
            cols = st.columns(3)
            grupo = datos_dolar[i:i+3]
            for j, d in enumerate(grupo):
                with cols[j]:
                    st.metric(
                        label=d['nombre'], 
                        value=f"${d['venta']:,.2f}", 
                        delta=f"Compra: ${d['compra']:,.0f}",
                        delta_color="normal"
                    )

# --- SECCIÓN 2: CUOTAS VS CONTADO ---
elif opcion == "Cuotas vs Contado":
    st.header("⚖️ Simulador: ¿Cuotas o Contado?")
    # (Aquí va la lógica que ya teníamos mejorada)
    p_contado = st.number_input("Precio de Contado ($)", value=100000.0)
    p_cuotas = st.number_input("Precio Total en Cuotas ($)", value=125000.0)
    cuotas = st.slider("Cantidad de cuotas", 1, 24, 12)
    inf = st.slider("Inflación mensual esperada (%)", 0.0, 15.0, 4.0)
    
    valor_cuota = p_cuotas / cuotas
    tasa = inf / 100
    va_total = sum([valor_cuota / ((1 + tasa) ** t) for t in range(1, cuotas + 1)])
    
    st.metric("Costo Real (Valor Actual)", f"${va_total:,.2f}")
    if va_total < p_contado:
        st.success("✅ Conviene financiar")
    else:
        st.error("❌ Conviene contado")

# --- SECCIÓN 3: CARRY TRADE ---
elif opcion == "Carry Trade (Bicicleta)":
    st.header("🚲 Simulador de Carry Trade")
    st.write("¿Conviene vender dólares, hacer tasa en pesos y volver al dólar?")
    
    # Intentamos sacar el precio del Blue para el cálculo
    blue_price = 1000.0 # Default
    if datos_dolar:
        blue_price = next(d['venta'] for d in datos_dolar if d['casa'] == 'blue')

    col1, col2 = st.columns(2)
    usd_vender = col1.number_input("Dólares a vender (USD)", value=1000.0)
    tasa_pf = col2.number_input("TNA Plazo Fijo (%)", value=40.0)
    plazo_dias = st.slider("Días de inversión", 30, 180, 30)
    usd_futuro = st.number_input("Precio esperado del dólar al finalizar", value=blue_price * 1.05)

    # Lógica
    pesos_iniciales = usd_vender * (blue_price * 0.98) # Estimando precio compra
    interes_ganado = pesos_iniciales * (tasa_pf/100 * plazo_dias / 365)
    pesos_finales = pesos_iniciales + interes_ganado
    usd_finales = pesos_finales / usd_futuro
    
    ganancia_neta = usd_finales - usd_vender
    
    st.divider()
    st.subheader(f"Resultado tras {plazo_dias} días")
    st.metric("Dólares finales", f"USD {usd_finales:,.2f}", delta=f"{ganancia_neta:,.2f} USD")
    
    if ganancia_neta > 0:
        st.success(f"El carry trade fue exitoso. Ganaste {ganancia_neta:,.2f} USD.")
    else:
        st.error("El dólar subió más que la tasa. Perdiste poder adquisitivo.")
