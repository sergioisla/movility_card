import requests
import pandas as pd
import altair as alt

import streamlit as st
import os
from PIL import Image

#API_HOST = os.getenv("API_HOST")

# Setting the wide config for the page
st.set_page_config(layout="wide")
#adding marging specs for the main page with css inyection
margins_css = """
    <style>
        .main > div {
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 0.5rem;
        }
    </style>
"""

st.markdown(margins_css, unsafe_allow_html=True)

#Title
st.markdown("""
    ## 🇲🇽 Mexico City
    ### Do Become a Statistic""")

col1, col2 = st.columns([1,1])

with col1:
    ## Safety Map Front
    st.markdown("""
    columna1 """)

with col2:
    st.markdown("""
    columna2 )
    """)

st.markdown("""
Selecciona un año:""")
checkbox_values = {'Year': [2020, 2021, 2022, 2023, 2024],}
selected_values = {}
for checkbox_label, checkbox_options in checkbox_values.items():
        selected_values[checkbox_label] = st.multiselect(checkbox_label, checkbox_options)


year = selected_values['Year']

st.markdown("""
Ingresa tu número de tarjeta de movilidad""")

num_tarj = st.text_input("Número de tarjeta de movilidad", max_chars=8)




cookies = {
}

headers = {
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://app.semovi.cdmx.gob.mx',
    'pragma': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

json_data = {
    'serie': num_tarj,
    'anio': year,
    'operacion': 'todas',
}

response = requests.post(
    'https://app.semovi.cdmx.gob.mx/micrositio/291-trazabilidad_tarjetas.php',
    headers=headers,
    json=json_data,
)
df = pd.DataFrame(response.json()["data"])
df.monto = df.monto.astype(float)
df.saldo_final = df.saldo_final.astype(float)
df['fecha'] = pd.to_datetime(df['fecha'],dayfirst=True)
df['mes'] = df['fecha'].dt.month
df_recarga = df.loc[df['operacion'] == "00-RECARGA"]
df_validacion = df.loc[df['operacion'] == "03-VALIDACION"]

count_stns = pd.DataFrame(df_validacion.value_counts('estacion'))
count_stns.reset_index(inplace=True)
count_stns.columns = ['estación', 'viajes']

total_recargas = df_recarga['monto'].sum()
total_validacion = df_validacion['monto'].sum()
st.markdown("""
Total de recargas en el año 2024 en pesos:""")
st.markdown(total_recargas)

st.markdown("""
Total gastado en el año 2024 en pesos:""")
st.markdown(total_validacion)

# Display the plot in Streamlit


st.markdown("""
Total de viajes en el año 2024 por estación:""")
altair_chart = alt.Chart(count_stns).mark_bar().encode(
    x='viajes:Q',
    y=alt.Y('estación:N', sort='-x', axis=alt.Axis(labelFontSize=12, labelPadding=30,labelLimit=200))

    ).properties(
    width=600,
    height=400
)


st.altair_chart(altair_chart)
