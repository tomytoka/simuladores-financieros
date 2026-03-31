import streamlit as st
import requests

# Configuración de página
st.set_page_config(page_title="UADE Finance Hub", page_icon="📈")

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
    if datos_dolar:
        cols = st.columns(len(datos_dolar))
        for i, d in enumerate(datos_dolar):
            with cols[i % 3]: # Organiza en columnas
                st.metric(label=d['nombre'], value=f"${d['venta']}", delta=f"Compra: ${d['compra']}")
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
