import streamlit as st
import pandas as pd

# Función para convertir strings tipo "Q 150,000.00" a float
def convertir_a_numero(valor):
    if valor:
        valor = valor.replace("Q", "").replace(",", "").strip()
        try:
            return float(valor)
        except:
            return 0.0
    return 0.0

# Título
st.title("Tablero de Pedidos")

# Inputs
pedido_input = st.text_input("Pedido: ")
descripcion_input = st.text_input("Descripción: ")
pago_input = st.text_input("Pago/Abono: ")
fecha_input = st.text_input("Fecha: ")

operacion_input = st.radio("Operación:", ["TRANSFERENCIA", "ACH", "DEPÓSITO"])
agencia_input = st.radio("Agencia:", ["BANRURAL", "BANCO INDUSTRIAL", "BANGO GYT", "BANTRAB"])
documento_input = st.text_input("No. documento:")

col1, col2 = st.columns(2)
with col1:
    debito_input = st.text_input("Débito:", key="debito", placeholder="Q 0.00")
with col2:
    credito_input = st.text_input("Crédito:", key="credito", placeholder="Q 0.00")

# Crear dataframe inicial
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=[
        "Número de Pedido", "Descripción", "Pago/Abono", "Agencia",
        "Fecha", "Operación", "No. documento", "Débito", "Crédito", "Apertura"
    ])

# Botón agregar pedido
if st.button("Agregar detalles del Pedido"):
    if pedido_input.strip() != "":
        debito_val = convertir_a_numero(debito_input)
        credito_val = convertir_a_numero(credito_input)
        
        # Calculamos Apertura acumulada
        if st.session_state.pedidos.empty:
            apertura_val = debito_val - credito_val
        else:
            apertura_val = debito_val - credito_val + st.session_state.pedidos["Apertura"].iloc[-1]
        
        nuevo_pedido = pd.DataFrame({
            "Número de Pedido": [pedido_input],
            "Descripción": [descripcion_input],
            "Pago/Abono": [pago_input],
            "Agencia": [agencia_input],
            "Fecha": [fecha_input],
            "Operación": [operacion_input],
            "No. documento": [documento_input],
            "Débito": [debito_val],
            "Crédito": [credito_val],
            "Apertura": [apertura_val]
        })
        
        st.session_state.pedidos = pd.concat([st.session_state.pedidos, nuevo_pedido], ignore_index=True)
        st.success(f"Pedido {pedido_input} agregado")
    else:
        st.error("Por favor, ingrese un número de pedido válido")

# Mostrar tabla
st.subheader("Pedidos Ingresados")
column_order = [
    "Número de Pedido", "Descripción", "Pago/Abono", "Agencia",
    "Fecha", "Operación", "No. documento", "Débito", "Crédito", "Apertura"
]
column_order_existente = [col for col in column_order if col in st.session_state.pedidos.columns]
st.dataframe(st.session_state.pedidos[column_order_existente], height=600)
