import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
from datetime import datetime
import altair as alt
import numpy as np
from folium.plugins import MarkerCluster

@st.cache_data()
def load_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    select_columnas = ['Year', 'OFNS_DESC','CMPLNT_FR_DT','CMPLNT_FR_TM','BORO_NM','SUSP_AGE_GROUP','SUSP_RACE','SUSP_SEX','VIC_AGE_GROUP','VIC_RACE','VIC_SEX','Latitude','Longitude']
    df = df[select_columnas]
    return df


def pagina_tiempo():
    st.title("Pagina Principal")
    st.write("Pagina de Principal")
    st.sidebar.header("Opciones a filtrar:") #sidebar lo que nos va a hacer es crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
    df = load_data("NYPD_2018_2023_FELONY_Q.csv")

    #ajuste fecha y hora
    df['CMPLNT_FR_DT'] = pd.to_datetime(df['CMPLNT_FR_DT'], format='%m/%d/%Y')
    df['CMPLNT_FR_TM'] = pd.to_datetime(df['CMPLNT_FR_TM'], format='%H:%M:%S').dt.strftime('%H:%M:%S')
     
    #SELECTORES  

    fecha_inicio_selector_p = st.sidebar.date_input('Fecha de inicio', value=datetime(2023,1,1).date(), key="date1")
    fecha_fin_selector_p = st.sidebar.date_input('Fecha de fin', value=datetime(2023,2,1).date() , key="date2")
    
    #selectores fechas
    fecha_inicio_selector = pd.to_datetime(fecha_inicio_selector_p)
    fecha_fin_selector = pd.to_datetime(fecha_fin_selector_p)

    tipo_delito_selector_ch = st.sidebar.selectbox(
        'Seleccionar tipo de crimen', 
        ['All'] + list(df['OFNS_DESC'].unique()))
    
    # sele por incidentes seleccionados
    tipo_delito_selector = st.sidebar.multiselect(
        "Seleccione un delito:",
        options = df['OFNS_DESC'].unique()
    )
    # Filtrar por municipios seleccionados
    municipio_selector = st.sidebar.multiselect(
        "Seleccione un municipio:",
        options = df['BORO_NM'].unique()
    )

    # Filtrar por edad sospechoso seleccionados
    edad_sosp_selector = st.sidebar.multiselect(
        "Seleccione edad sospechoso:",
        options = df['SUSP_AGE_GROUP'].unique()
    )

    # Filtrar por raza sospechoso seleccionados
    raza_sosp_selector = st.sidebar.multiselect(
        "Seleccione raza sospechoso:",
        options = df['SUSP_RACE'].unique()
    )

    # Filtrar sexo sospechoso seleccionados
    sexo_sosp_selector = st.sidebar.multiselect(
        "Seleccione un sexo Sospechoso:",
        options = df['SUSP_SEX'].unique()
    )
    '''
    # Filtrar por edad victima seleccionados
    edad_vic_selector = st.sidebar.multiselect(
        "Seleccione edad victima:",
        options = df['VIC_AGE_GROUP'].unique()
    )

    # Filtrar por raza victima seleccionados
    raza_vic_selector = st.sidebar.multiselect(
        "Seleccione raza victima:",
        options = df['VIC_RACE'].unique()
    )

    # Filtrar sexo victima seleccionados
    sexo_vic_selector = st.sidebar.multiselect(
        "Seleccione un sexo victima:",
        options = df['VIC_SEX'].unique()
    )
    '''
    

      # Filtro de fechas
    #filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) & (df['CMPLNT_FR_DT'] <= fecha_fin_selector)]
    
    #filtered_df = filtered_df[filtered_df['OFNS_DESC'].isin(tipo_delito_selector)]
    
    
    ###Aqui es donde pasa la MAGIA. conectar los selectores con la base de datos

    if fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and edad_sosp_selector and raza_sosp_selector and sexo_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and edad_sosp_selector and raza_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and raza_sosp_selector and sexo_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and edad_sosp_selector and sexo_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
        
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and edad_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and sexo_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
        
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and raza_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                        (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                        (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                        (df['BORO_NM'].isin(municipio_selector)) &
                        (df['SUSP_RACE'].isin(raza_sosp_selector)) 
                        ]  
    ####
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and edad_sosp_selector and raza_sosp_selector and sexo_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]

    elif fecha_inicio_selector and fecha_fin_selector and  tipo_delito_selector and edad_sosp_selector and raza_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and fecha_fin_selector and tipo_delito_selector and edad_sosp_selector and sexo_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector  and raza_sosp_selector and sexo_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector  and edad_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector  and sexo_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
        
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector  and raza_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                        (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                        (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                        (df['SUSP_RACE'].isin(raza_sosp_selector)) 
                        ]  
    
    ####
    elif fecha_inicio_selector and  fecha_fin_selector and municipio_selector and edad_sosp_selector and raza_sosp_selector and sexo_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
        
    elif fecha_inicio_selector and  fecha_fin_selector and  municipio_selector and edad_sosp_selector and raza_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  municipio_selector and edad_sosp_selector and sexo_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  municipio_selector  and raza_sosp_selector and sexo_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  municipio_selector  and edad_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  municipio_selector  and sexo_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
        
    elif fecha_inicio_selector and  fecha_fin_selector and  municipio_selector  and raza_sosp_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                        (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                        (df['BORO_NM'].isin(municipio_selector)) &
                        (df['SUSP_RACE'].isin(raza_sosp_selector)) 
                        ]  
        
    ###
        
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector: #todos
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector))
                        ]
    elif fecha_inicio_selector and fecha_fin_selector and tipo_delito_selector: 
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector))
                        ]
    elif fecha_inicio_selector and  fecha_fin_selector and municipio_selector: 
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector))
                        ]
    elif  tipo_delito_selector and municipio_selector:
        filtered_df = df[(df['OFNS_DESC'].isin(tipo_delito_selector)) & 
                         (df['BORO_NM'].isin(municipio_selector)) 
                         ]
    elif fecha_inicio_selector and fecha_fin_selector:
        filtered_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) & (df['CMPLNT_FR_DT'] <= fecha_fin_selector)]
    elif  tipo_delito_selector:
        filtered_df = df[df['OFNS_DESC'].isin(tipo_delito_selector)]
    elif  municipio_selector:
        filtered_df = df[df['BORO_NM'].isin(municipio_selector)]
    else:
        filtered_df = df
    

    
    with st.container():
        st.write(fecha_inicio_selector)
        st.write(fecha_fin_selector)
        st.write(tipo_delito_selector)
        st.write(df.head())
        st.write(len(df))
        st.write("-------------------")
        st.write("filtrado")
        st.write(filtered_df.head())
        st.write(len(filtered_df))
        st.write("..pther...")
        delitos_edad_df = filtered_df[['OFNS_DESC','SUSP_AGE_GROUP']]

        # Realizar el conteo de ocurrencias
        delitos_edad_g_df = pd.crosstab(index=delitos_edad_df['SUSP_AGE_GROUP'], columns=delitos_edad_df['OFNS_DESC'])
        all_columns = delitos_edad_df['OFNS_DESC'].unique()
        delitos_edad_g_df = delitos_edad_g_df.reindex(columns=all_columns, fill_value=0)
        delitos_edad_g_df.index.name = 'Age'
        delitos_edad_g_df = delitos_edad_g_df.reset_index()
        #delitos_anios_df=delitos_anios_df.groupby('OFNS_DESC','SUSP_AGE_GROUP').count()
        st.write(delitos_edad_g_df.head())

        #grafica
        multi_line = alt.Chart(delitos_edad_g_df).transform_fold(tipo_delito_selector).mark_line().encode(
        x=alt.X('Age:O', title="Edad"),
        y=alt.Y('value:Q', title="Numero de sospechosos"),
        color='key:N').properties(
        title='Sospechoso de crime por edad',
        width=700,
        height=450).interactive()
        st.write(multi_line)

        #otraa

        mean_x = np.mean(filtered_df["Latitude"])
        mean_y = np.mean(filtered_df["Longitude"])

        m = folium.Map(location = [mean_y, mean_x])
        marker_cluster = MarkerCluster().add_to(m)

        for index, row in filtered_df.iterrows():

            folium.CircleMarker([row["Latitude"], row["Longitude"]], popup = row["OFNS_DESC"], fill = True).add_to(marker_cluster)

        folium_static(m,width = 1000)