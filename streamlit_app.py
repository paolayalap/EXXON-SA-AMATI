
import streamlit as st
import pandas as pd

# Título de la app
st.title("Tablero de Pedidos")

# Crear un lugar para ingresar el número de pedido
pedido_input = st.text_input("Pedido: ")

# Crear un dataframe para almacenar los pedidos
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=["Número de Pedido"])

# Botón para agregar el pedido
if st.button("Agregar Pedido"):
    if pedido_input.strip() != "":
        # Agregar al dataframe
        st.session_state.pedidos = pd.concat(
            [st.session_state.pedidos, pd.DataFrame({"Número de Pedido": [pedido_input]})],
            ignore_index=True
        )
        st.success(f"Pedido {pedido_input} agregado")
    else:
        st.error("Por favor, ingrese un número de pedido válido")

# Mostrar la tabla de pedidos
st.subheader("Pedidos Ingresados")
st.dataframe(st.session_state.pedidos)
