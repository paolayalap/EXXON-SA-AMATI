import streamlit as st
import pandas as pd

# Título de la app
st.title("Tablero de Pedidos")

# Inputs para cada campo
pedido_input = st.text_input("Pedido: ")
descripcion_input = st.text_input("Descripción: ")
pago_input = st.text_input("Pago/Abono: ")
fecha_input = st.text_input("Fecha: ")

# Radio buttons para Operación
operacion_input = st.radio("Operación:", ["TRANSFERENCIA", "ACH", "DEPÓSITO"])

# Radio buttons para Agencia
agencia_input = st.radio("Agencia:", ["BANRURAL", "BANCO INDUSTRIAL", "BANGO GYT", "BANTRAB"])

documento_input = st.text_input("No. documento: ")

# Inputs para Débito y Crédito con color usando CSS
st.markdown("""
<style>
input.debito {background-color: #d4edda !important;}   /* verde claro */
input.credito {background-color: #f8d7da !important;}  /* rojo claro */
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    debito_input = st.text_input("Débito:", key="debito", placeholder="Q 0.00")
with col2:
    credito_input = st.text_input("Crédito:", key="credito", placeholder="Q 0.00")

# --- CREAR DATAFRAME INICIAL CON TODAS LAS COLUMNAS ---
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=[
        "Número de Pedido", "Descripción", "Pago/Abono", "Agencia",
        "Fecha", "Operación", "No. documento", "Débito", "Crédito"
    ])

# Botón para agregar el pedido
if st.button("Agregar detalles del Pedido"):
    if pedido_input.strip() != "":
        nuevo_pedido = pd.DataFrame({
            "Número de Pedido": [pedido_input],
            "Descripción": [descripcion_input],
            "Pago/Abono": [pago_input],
            "Agencia": [agencia_input],
            "Fecha": [fecha_input],
            "Operación": [operacion_input],
            "No. documento": [documento_input],
            "Débito": [debito_input],
            "Crédito": [credito_input]
        })
        st.session_state.pedidos = pd.concat([st.session_state.pedidos, nuevo_pedido], ignore_index=True)
        st.success(f"Pedido {pedido_input} agregado")
    else:
        st.error("Por favor, ingrese un número de pedido válido")

# --- MOSTRAR TABLA ---
st.subheader("Pedidos Ingresados")

# Validar que las columnas existen antes de mostrar
column_order = ["Número de Pedido", "Descripción", "Pago/Abono", "Agencia",
                "Fecha", "Operación", "No. documento", "Débito", "Crédito"]

# Filtrar solo las columnas que realmente existen en el dataframe
column_order_existente = [col for col in column_order if col in st.session_state.pedidos.columns]

st.dataframe(st.session_state.pedidos[column_order_existente])
