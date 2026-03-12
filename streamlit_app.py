import streamlit as st
import pandas as pd

# Título de la app
st.title("Tablero de Pedidos")

# Inputs de texto
pedido_input = st.text_input("Pedido: ")
descripcion_input = st.text_input("Descripción: ")
pago_input = st.text_input("Pago/Abono: ")
fecha_input = st.text_input("Fecha: ")

# Radio buttons para Operación
operacion_input = st.radio("Operación:", ["TRANSFERENCIA", "ACH", "DEPÓSITO"])

# Selección de Agencia con imágenes
st.subheader("Agencia:")
col1, col2, col3, col4 = st.columns(4)

agencia_input = None

with col1:
    st.image("imagenes/banco_gyt.png", width=100)
    if st.button("BANGO GYT"):
        agencia_input = "BANGO GYT"

with col2:
    st.image("imagenes/banco_industrial.png", width=100)
    if st.button("BANCO INDUSTRIAL"):
        agencia_input = "BANCO INDUSTRIAL"

with col3:
    st.image("imagenes/banrural.png", width=100)
    if st.button("BANRURAL"):
        agencia_input = "BANRURAL"

with col4:
    st.image("imagenes/bantrab.png", width=100)
    if st.button("BANTRAB"):
        agencia_input = "BANTRAB"

# Input de documento
documento_input = st.text_input("No. documento: ")

# Crear el dataframe para almacenar los pedidos
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=[
        "Número de Pedido", "Descripción", "Pago/Abono", "Fecha", "Operación", "Agencia", "No. documento"
    ])

# Botón para agregar el pedido
if st.button("Agregar detalles del Pedido"):
    if pedido_input.strip() != "":
        if agencia_input is None:
            st.error("Por favor, seleccione una agencia")
        else:
            nuevo_pedido = pd.DataFrame({
                "Número de Pedido": [pedido_input],
                "Descripción": [descripcion_input],
                "Pago/Abono": [pago_input],
                "Fecha": [fecha_input],
                "Operación": [operacion_input],
                "Agencia": [agencia_input],
                "No. documento": [documento_input]
            })
            st.session_state.pedidos = pd.concat([st.session_state.pedidos, nuevo_pedido], ignore_index=True)
            st.success(f"Pedido {pedido_input} agregado")
    else:
        st.error("Por favor, ingrese un número de pedido válido")

# Mostrar tabla de pedidos
st.subheader("Pedidos Ingresados")
st.dataframe(st.session_state.pedidos)

