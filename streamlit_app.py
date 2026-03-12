import streamlit as st
import pandas as pd

# Título de la app
st.title("Tablero de Pedidos")

# Crear inputs para cada campo
pedido_input = st.text_input("Pedido: ")
descripcion_input = st.text_input("Descripción: ")
pago_input = st.text_input("Pago/Abono: ")
fecha_input = st.text_input("Fecha: ")

# Radio buttons para Operación
operacion_input = st.radio("Operación:", ["TRANSFERENCIA", "ACH", "DEPÓSITO"])

# Radio buttons para Agencia
agencia_input = st.radio("Agencia:", ["BANRURAL", "BANCO INDUSTRIAL", "BANGO GYT", "BANTRAB"])

documento_input = st.text_input("No. documento: ")

# Crear un dataframe para almacenar los pedidos
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=[
        "Número de Pedido", "Descripción", "Pago/Abono", "Agencia", "Fecha", "Operación", "No. documento"
    ])

# Botón para agregar el pedido
if st.button("Agregar detalles del Pedido"):
    if pedido_input.strip() != "":
        # Agregar al dataframe
        nuevo_pedido = pd.DataFrame({
            "Número de Pedido": [pedido_input],
            "Descripción": [descripcion_input],
            "Pago/Abono": [pago_input],
            "Agencia": [agencia_input],
            "Fecha": [fecha_input],
            "Operación": [operacion_input],
            "No. documento": [documento_input]
        })
        st.session_state.pedidos = pd.concat([st.session_state.pedidos, nuevo_pedido], ignore_index=True)
        st.success(f"Pedido {pedido_input} agregado")
    else:
        st.error("Por favor, ingrese un número de pedido válido")

# Mostrar la tabla de pedidos
st.subheader("Pedidos Ingresados")
st.dataframe(st.session_state.pedidos)
