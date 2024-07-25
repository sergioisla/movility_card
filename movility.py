import requests
import pandas as pd
import altair as alt

import streamlit as st
import os
from PIL import Image



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
    ##
    ### Aquí puedes revisar la información de tu tarjeta de movilidad de la CDMX por año""")
#Option to write something in a pair of columns
col1, col2 = st.columns([1,1])

with col1:
    ## Safety Map Front
    st.markdown("""
     """)

with col2:
    st.markdown("""

    """)


#Card number input
st.markdown("""
""")
num_tarj = st.text_input("Ingresa los 8 últimos dígitos de tu tarjeta de movilidad:", max_chars=8)

#Year input
st.markdown("""
""")
anio = st.text_input("Ingresa un año del 2020 al 2024:", max_chars=4)

#Retrieve data from the official website
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
    'anio': anio,
    'operacion': 'todas',
}

response = requests.post(
    'https://app.semovi.cdmx.gob.mx/micrositio/291-trazabilidad_tarjetas.php',
    headers=headers,
    json=json_data,
)

df = pd.DataFrame(response.json()["data"])

#In case there is no data
if df.shape == (1,1):
    st.markdown("""
    No hay datos en el año elegido""")
else:
    #Some columns transformation
    df.monto = df.monto.astype(float)
    df.saldo_final = df.saldo_final.astype(float)
    df['fecha'] = pd.to_datetime(df['fecha'],dayfirst=True)
    df['mes'] = df['fecha'].dt.month

    #Filtering data about money added to the card
    df_recarga = df.loc[df['operacion'] == "00-RECARGA"]

    #Filtering data about money spent by the card
    df_validacion = df.loc[df['operacion'] == "03-VALIDACION"]

    #Preparing data to be used to plot trips by station
    count_stns = pd.DataFrame(df_validacion.value_counts('estacion'))
    count_stns.reset_index(inplace=True)
    count_stns.columns = ['Estación', 'Viajes']

    #Preparing data to be used to plot trips by month
    count_mes = pd.DataFrame(df_validacion.value_counts('mes'))
    count_mes.reset_index(inplace=True)
    count_mes.columns = ['Mes', 'Viajes']
    count_mes.sort_values('Mes',inplace=True)
    count_mes['Mes'] = pd.to_datetime(count_mes['Mes'], format='%m').dt.strftime('%b')
    look_up = {'Jan': '01-Enero', 'Feb': '02-Febrero', 'Mar': '03-Marzo', 'Apr': '04-Abril', 'May': '05-Mayo',
            'Jun': '06-Junio', 'Jul': '07-Julio', 'Aug': '08-Agosto', 'Sep': '09-Septiembre', 'Oct': '10-Octubre', 'Nov': '11-Noviembre', 'Dec': '12-Diciembre'}
    count_mes['Mes'] = count_mes['Mes'].apply(lambda x: look_up[x])

    #Sum of money added to the card
    total_recargas = df_recarga['monto'].sum()

    #Sum of money spent by the card
    total_validacion = df_validacion['monto'].sum()

    st.markdown(""" \n """)

    #Display money added and spent
    st.markdown(f"##### Total de recargas durante {anio}: &nbsp;&nbsp;  ${total_recargas}")
    st.markdown(f"##### Total gastado durante {anio}:  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${total_validacion}")
    st.markdown(""" \n """)
    st.markdown(""" \n """)

    # Display the plot about trips by station
    st.markdown(f"##### Total de viajes por estación durante {anio}:")
    altair_chart_stns = alt.Chart(count_stns).mark_bar().encode(
        x='Viajes:Q',
        y=alt.Y('Estación:N', sort='-x', axis=alt.Axis(labelFontSize=12, labelPadding=30,labelLimit=200))
        ).properties(
        width=300,
        height=500
    )
    st.altair_chart(altair_chart_stns)

    # Display the plot about trips by month
    st.markdown(f"##### Total de viajes por mes durante {anio}:")
    altair_chart_mes = alt.Chart(count_mes).mark_bar().encode(
        x='Mes',
        y='Viajes'
        ).properties(
        width=300,
        height=400
    )
    st.altair_chart(altair_chart_mes)
