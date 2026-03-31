import streamlit as st
import requests

# Configuración de página (NOMBRE DE TU PROYECTO)
st.set_page_config(page_title="My Finance Lab", page_icon="📊", layout="wide")

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

st.title("🚀 Finance Lab")
st.write("Herramientas interactivas para análisis financiero y toma de decisiones.")

# --- FUNCIÓN PARA OBTENER DÓLAR ---
def obtener_dolares():
    try:
        url = "https://dolarapi.com/v1/dolares"
        res = requests.get(url)
        return res.json()
    except:
        return None

# --- MENÚ LATERAL ---
st.sidebar.title("Navegación")
opcion = st.sidebar.selectbox("Elegí un simulador", 
    ["Cotizaciones en Tiempo Real", "Cuotas vs Contado", "Carry Trade (Bicicleta)"])

datos_dolar = obtener_dolares()

# --- SECCIÓN 1: COTIZACIONES ---
if opcion == "Cotizaciones en Tiempo Real":
    st.header("💵 Cotizaciones Actuales (Argentina)")
    st.write("Datos en tiempo real extraídos de DolarApi.")

    if datos_dolar:
        # Creamos filas de a 3 columnas para que no se amontonen
        for i in range(0, len(datos_dolar), 3):
            cols = st.columns(3)
            # Agarramos un grupo de 3 dólares
            grupo = datos_dolar[i:i+3]
            
            for j, d in enumerate(grupo):
                with cols[j]:
                    # Formateamos el precio para que se vea limpio
                    precio_vta = f"${d['venta']:,.2f}"
                    precio_compra = f"Compra: ${d['compra']:,.0f}"
                    
                    st.metric(
                        label=d['nombre'], 
                        value=precio_vta, 
                        delta=precio_compra,
                        delta_color="normal" # Esto lo pone en verde/gris según el valor
                    )
    else:
        st.error("No se pudieron cargar los datos. Reintentá en unos minutos.")

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
