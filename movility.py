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
    ## 🇲🇽 Mexico City - Safety Map
    ### Don't Become a Statistic""")

col1, col2 = st.columns([1,1])

with col1:
    ## Safety Map Front
    st.markdown("""
    Despite our love for CDMX, we cannot ignore the fact that it is not the safest place on earth.\n
    However, we are here to empower you with amazing knowledge and provide a safety map for this incredible city.\n
    Our aim is to offer a comprehensive overview of neighborhoods where you can enjoy tacos and mezcal without worries,
    as well as areas where caution is advised.""")

with col2:
    st.markdown("""
    Our data encompasses all registered crimes in the Colonias of CDMX from **2019 to 2023**. By sharing this information, we hope to help you make informed decisions and navigate the city with confidence.\n
    Remember, being aware is the first step towards safety. Let us guide you through the vibrant streets of CDMX, ensuring that you won't become just another statistic.\n
    To be transparent from the beginning, you can find the data for our project publicly available [here](https://datos.cdmx.gob.mx/dataset/victimas-en-carpetas-de-investigacion-fgj#:~:text=Descargar-,V%C3%ADctimas%20en%20Carpetas%20de%20Investigaci%C3%B3n%20(completa),-CSV)
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

total_recargas = df_recarga['monto'].sum()

st.markdown("""
Total de recargas en el año:""")

st.markdown(total_recargas)
# Display the plot in Streamlit

#altair_chart = alt.Chart(df_validacion).mark_bar().encode(
    x='estacion',
    #y='b'
)

#st.altair_chart(altair_chart, use_container_width=False, theme="streamlit", key=None, on_select="ignore", selection_mode=None)
