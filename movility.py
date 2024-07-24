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
    Despite """)

with col2:
    st.markdown("""
    Our data )
    """)


st.markdown("""
Ingresa tu número de tarjeta de movilidad""")

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
    'anio': '2024',
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

st.markdown("""
Total de recargas en el año:""")

st.markdown(total_recargas)
# Display the plot in Streamlit

altair_chart = alt.Chart(count_stns).mark_bar().encode(
    x='viajes',
    y='estación'
    ).properties(
    width=600,
    height=400
)

st.altair_chart(altair_chart)
