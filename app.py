import streamlit as st

st.set_page_config(page_title="Simulador Financiero UADE", layout="centered")

st.title("⚖️ ¿Cuotas o Contado?")
st.write("Calculá si te conviene pagar hoy o financiar según la inflación esperada.")

st.sidebar.header("Configuración")

# Inputs del usuario
precio_contado = st.number_input("Precio de Contado ($)", min_value=0.0, value=100000.0)
precio_cuotas = st.number_input("Precio Total en Cuotas ($)", min_value=0.0, value=120000.0)
cant_cuotas = st.slider("Cantidad de cuotas", 1, 24, 12)
inflacion_mensual = st.slider("Inflación mensual esperada (%)", 0.0, 20.0, 4.0)

# Cálculo financiero (Valor Actual de las cuotas)
valor_cuota = precio_cuotas / cant_cuotas
tasa = inflacion_mensual / 100

# Calculamos el Valor Actual Neto (VAN) de las cuotas
valor_actual_total = 0
for t in range(1, cant_cuotas + 1):
    valor_actual_total += valor_cuota / ((1 + tasa) ** t)

st.divider()

# Resultados
col1, col2 = st.columns(2)
col1.metric("Costo Real (Valor Actual)", f"${valor_actual_total:,.2f}")
col2.metric("Ahorro / Pérdida", f"${precio_contado - valor_actual_total:,.2f}")

if valor_actual_total < precio_contado:
    st.success(f"✅ ¡Conviene pagar en **{cant_cuotas} cuotas**! El valor real es menor que el contado.")
else:
    st.error("❌ Conviene pagar de **Contado**. La inflación no llega a licuar las cuotas.")

st.info(f"Este cálculo asume una inflación constante del {inflacion_mensual}% mensual.")
