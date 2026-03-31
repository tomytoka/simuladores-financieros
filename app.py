import streamlit as st
import requests

# 1. CONFIGURACIÓN (Una sola vez y al principio)
st.set_page_config(page_title="Finance Lab", page_icon="📊", layout="wide")

# 2. ESTILO CSS (Limpio y moderno)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #050505;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(0, 168, 232, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(50, 255, 126, 0.05) 0%, transparent 40%);
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px !important;
        border-radius: 20px;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        border: 1px solid rgba(50, 255, 126, 0.3);
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.05);
    }

    [data-testid="stMetricValue"] div {
        color: #32ff7e !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. FUNCIONES DE AYUDA
def obtener_dolares():
    try:
        url = "https://dolarapi.com/v1/dolares"
        res = requests.get(url)
        return res.json()
    except:
        return None

# 4. BARRA LATERAL (Definimos las variables primero)
st.sidebar.title("Navegación")
opcion = st.sidebar.selectbox("Elegí un simulador", 
    ["Cotizaciones", "Cuotas vs Contado", "Carry Trade"])

st.sidebar.divider()
st.sidebar.markdown("### **Desarrollado por Tomas Tokatlian**")
st.sidebar.write("Estudiante de Lic. en Finanzas")

# Obtenemos los datos una sola vez
datos_dolar = obtener_dolares()

# 5. CONTENIDO PRINCIPAL
if opcion == "Cotizaciones":
    st.title("💵 Mercado de Cambios")
    st.write("Precios de referencia en tiempo real.")
    st.write("---")

    if datos_dolar:
        for i in range(0, len(datos_dolar), 3):
            cols = st.columns(3)
            grupo = datos_dolar[i:i+3]
            for j, d in enumerate(grupo):
                with cols[j]:
                    st.metric(
                        label=d['nombre'], 
                        value=f"${d['venta']:,.2f}", 
                        delta=f"Compra: ${d['compra']:,.0f}"
                    )
            st.write("") 
    else:
        st.error("No se pudo conectar con la API de cotizaciones.")

elif opcion == "Cuotas vs Contado":
    st.title("⚖️ Cuotas vs Contado")
    st.write("Evaluá el impacto de la inflación en tus compras financiadas.")
    
    col1, col2 = st.columns(2)
    with col1:
        p_contado = st.number_input("Precio de Contado ($)", value=100000.0)
        p_cuotas = st.number_input("Precio Total en Cuotas ($)", value=125000.0)
    with col2:
        cuotas = st.slider("Cantidad de cuotas", 1, 24, 12)
        inf = st.slider("Inflación mensual esperada (%)", 0.0, 15.0, 4.0)
    
    valor_cuota = p_cuotas / cuotas
    tasa = inf / 100
    va_total = sum([valor_cuota / ((1 + tasa) ** t) for t in range(1, cuotas + 1)])
    
    st.write("---")
    st.metric("Costo Real (Valor de hoy)", f"${va_total:,.2f}", 
              delta=f"${va_total - p_contado:,.2f}", delta_color="inverse")
    
    if va_total < p_contado:
        st.success("✅ La inflación licúa las cuotas. ¡Conviene financiar!")
    else:
        st.error("❌ El recargo es muy alto. Conviene pagar de contado.")

elif opcion == "Carry Trade":
    st.title("🚲 Carry Trade")
    st.write("Simulador de arbitraje de tasa vs. devaluación.")
    
    blue_price = 1000.0
    if datos_dolar:
        # Buscamos el blue en la lista
        for d in datos_dolar:
            if "Blue" in d['nombre']:
                blue_price = d['venta']

    col1, col2 = st.columns(2)
    with col1:
        usd_vender = st.number_input("Dólares a vender (USD)", value=1000.0)
        tasa_pf = st.number_input("TNA Plazo Fijo (%)", value=40.0)
    with col2:
        plazo_dias = st.slider("Días de inversión", 30, 180, 30)
        usd_futuro = st.number_input("Precio esperado del dólar al final", value=blue_price * 1.05)

    pesos_iniciales = usd_vender * (blue_price * 0.98) # Precio compra aprox
    interes = pesos_iniciales * (tasa_pf/100 * plazo_dias / 365)
    usd_finales = (pesos_iniciales + interes) / usd_futuro
    ganancia = usd_finales - usd_vender
    
    st.write("---")
    st.metric("Resultado Final", f"USD {usd_finales:,.2f}", delta=f"{ganancia:,.2f} USD")
    
    if ganancia > 0:
        st.success(f"Ganancia de USD {ganancia:,.2f}")
    else:
        st.error(f"Pérdida de USD {abs(ganancia):,.2f}")
