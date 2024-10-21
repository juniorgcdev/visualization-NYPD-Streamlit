import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
#import folium
#from streamlit_folium import folium_static
#from folium.plugins import HeatMap
#importar paginas
#from st_pages import show_pages, hide_pages, Page
from paginas.cluster import pagina_cluster
from paginas.principal import pagina_principal
from paginas.mapas import pagina_mapas
from paginas.visualizacion import pagina_visualizacion
from paginas.robos import pagina_robos
from paginas.rango import pagina_rango
from paginas.anios import pagina_anios
from paginas.victima import pagina_victima
from paginas.sospechoso import pagina_sospechoso

st.set_page_config(
    page_title="NYP Dashboard",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded")
#hide_pages(
#    [
#       "test","app"
#    ]
#)

st.sidebar.title('👨‍💻👨‍💻NYP Dashboard')

st.title("Delitos graves: 2018-2023 en Nueva York")

#st.sidebar.markdown("<h1 style='text-align: center; color: black; marfin-top:-30px;'>Análisis de Patrones delictivos graves en New York</h1>", unsafe_allow_html=True)
lista_paginas = ["Pagina principal","Análisis por año","Rango de fecha","Análisis por sospechoso","Análisis por Victima","Visualización en Mapa"]
pagina = st.sidebar.selectbox("Seleccione una pagina",lista_paginas)
st.sidebar.divider()
if pagina == lista_paginas[0]:
    pagina_principal()
elif pagina ==lista_paginas[1]:
    pagina_anios()
elif pagina ==lista_paginas[2]:
    pagina_rango()
elif pagina ==lista_paginas[3]:
    pagina_sospechoso()
elif pagina ==lista_paginas[4]:
    pagina_victima()
elif pagina ==lista_paginas[5]:
    pagina_mapas()

