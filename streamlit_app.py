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

# Función para insertar filas en blanco al cambiar la fecha
def insertar_filas_blanco_por_fecha(df, columna_fecha="Fecha"):
    df_copy = df.copy()
    # Convertimos usando dayfirst=True para DD/MM/YYYY
    df_copy[columna_fecha] = pd.to_datetime(df_copy[columna_fecha], format="%d/%m/%Y", errors='coerce')
    
    new_rows = []
    prev_fecha = None
    for i, row in df_copy.iterrows():
        curr_fecha = row[columna_fecha].date() if pd.notnull(row[columna_fecha]) else None
        if prev_fecha is not None and curr_fecha != prev_fecha:
            # Insertar fila en blanco
            new_rows.append(pd.Series([None]*len(df.columns), index=df.columns))
        new_rows.append(row)
        prev_fecha = curr_fecha
    df_new = pd.DataFrame(new_rows).reset_index(drop=True)
    return df_new

# --- Inputs ---
st.title("Tablero de Pedidos")

pedido_input = st.text_input("Pedido: ")
descripcion_input = st.text_input("Descripción: ")
pago_input = st.text_input("Pago/Abono: ")
fecha_input = st.text_input("Fecha (DD/MM/YYYY): ", placeholder="DD/MM/YYYY")

operacion_input = st.radio("Operación:", ["TRANSFERENCIA", "ACH", "DEPÓSITO"])
agencia_input = st.radio("Agencia:", ["BANRURAL", "BANCO INDUSTRIAL", "BANGO GYT", "BANTRAB"])
documento_input = st.text_input("No. documento:")

col1, col2 = st.columns(2)
with col1:
    debito_input = st.text_input("Débito:", key="debito", placeholder="Q 0.00")
with col2:
    credito_input = st.text_input("Crédito:", key="credito", placeholder="Q 0.00")

# --- Dataframe inicial ---
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=[
        "Número de Pedido", "Descripción", "Pago/Abono", "Agencia",
        "Fecha", "Operación", "No. documento", "Débito", "Crédito", "Apertura"
    ])

# --- Botón agregar ---
if st.button("Agregar detalles del Pedido"):
    if pedido_input.strip() != "":
        debito_val = convertir_a_numero(debito_input)
        credito_val = convertir_a_numero(credito_input)
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

# --- Mostrar tabla ordenada por Fecha con filas en blanco ---
st.subheader("Pedidos Ingresados")
if not st.session_state.pedidos.empty:
    # Convertimos Fecha a datetime para ordenar
    df_sorted = st.session_state.pedidos.copy()
    df_sorted["Fecha_dt"] = pd.to_datetime(df_sorted["Fecha"], format="%d/%m/%Y", errors='coerce')
    df_sorted = df_sorted.sort_values(by="Fecha_dt").drop(columns=["Fecha_dt"]).reset_index(drop=True)

    # Insertar filas en blanco al cambiar de fecha
    df_mostrado = insertar_filas_blanco_por_fecha(df_sorted, columna_fecha="Fecha")

    column_order = [
        "Número de Pedido", "Descripción", "Pago/Abono", "Agencia",
        "Fecha", "Operación", "No. documento", "Débito", "Crédito", "Apertura"
    ]
    column_order_existente = [col for col in column_order if col in df_mostrado.columns]
    st.dataframe(df_mostrado[column_order_existente], height=600)
else:
    st.info("No hay pedidos agregados aún")
