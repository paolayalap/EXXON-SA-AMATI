import streamlit as st
import pandas as pd

def convertir_a_numero(valor):
    if valor:
        valor = valor.replace("Q", "").replace(",", "").strip()
        try:
            return float(valor)
        except:
            return 0.0
    return 0.0

def insertar_filas_blanco_por_fecha(df, columna_fecha="Fecha"):
    df_copy = df.copy()
    df_copy[columna_fecha] = pd.to_datetime(df_copy[columna_fecha], format="%d/%m/%Y", errors='coerce')
    new_rows = []
    prev_fecha = None
    for i, row in df_copy.iterrows():
        curr_fecha = row[columna_fecha].date() if pd.notnull(row[columna_fecha]) else None
        if prev_fecha is not None and curr_fecha != prev_fecha:
            new_rows.append(pd.Series([None]*len(df.columns), index=df.columns))
        new_rows.append(row)
        prev_fecha = curr_fecha
    df_new = pd.DataFrame(new_rows).reset_index(drop=True)
    return df_new

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

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=[
        "Número de Pedido", "Descripción", "Pago/Abono", "Agencia",
        "Fecha", "Operación", "No. documento", "Débito", "Crédito", "Apertura"
    ])

if st.button("Agregar detalles del Pedido"):
    if pedido_input.strip() != "":
        debito_val = convertir_a_numero(debito_input)
        credito_val = convertir_a_numero(credito_input)
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
            "Apertura": [0]  # temporal, se recalcula después
        })
        st.session_state.pedidos = pd.concat([st.session_state.pedidos, nuevo_pedido], ignore_index=True)
        st.success(f"Pedido {pedido_input} agregado")
    else:
        st.error("Por favor, ingrese un número de pedido válido")

# --- Recalcular Apertura después de ordenar por fecha ---
if not st.session_state.pedidos.empty:
    df_sorted = st.session_state.pedidos.copy()
    df_sorted["Fecha_dt"] = pd.to_datetime(df_sorted["Fecha"], format="%d/%m/%Y", errors='coerce')
    df_sorted = df_sorted.sort_values(by="Fecha_dt").reset_index(drop=True)
    
    # Recalcular Apertura acumulada
    apertura_acum = []
    for i, row in df_sorted.iterrows():
        debito_val = row["Débito"]
        credito_val = row["Crédito"]
        if i == 0:
            apertura_acum.append(debito_val - credito_val)
        else:
            apertura_acum.append((debito_val - credito_val) + apertura_acum[i-1])
    df_sorted["Apertura"] = apertura_acum
    
    # Insertar filas en blanco por cambio de fecha
    df_mostrado = insertar_filas_blanco_por_fecha(df_sorted, columna_fecha="Fecha")
    
    column_order = [
        "Número de Pedido", "Descripción", "Pago/Abono", "Agencia",
        "Fecha", "Operación", "No. documento", "Débito", "Crédito", "Apertura"
    ]
    column_order_existente = [col for col in column_order if col in df_mostrado.columns]
    st.subheader("Pedidos Ingresados")
    st.dataframe(df_mostrado[column_order_existente], height=600)

else:
    st.info("No hay pedidos agregados aún")


# --- Botón de descarga ---
import io

# Crear un buffer en memoria
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_mostrado[column_order_existente].to_excel(writer, index=False, sheet_name='Pedidos')
    writer.save()
output.seek(0)

# Botón de descarga
st.download_button(
    label="Descargar tabla como Excel",
    data=output,
    file_name="pedidos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
