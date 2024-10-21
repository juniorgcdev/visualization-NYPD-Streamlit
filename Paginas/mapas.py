import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import numpy as np
from datetime import datetime


@st.cache_data()
def load_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    select_columnas = ['Year', 'OFNS_DESC','CMPLNT_FR_DT','CMPLNT_FR_TM','BORO_NM','SUSP_AGE_GROUP','SUSP_RACE','SUSP_SEX','VIC_AGE_GROUP','VIC_RACE','VIC_SEX','Latitude','Longitude']
    df = df[select_columnas]
    df = df[df['OFNS_DESC'] != '(null)']
    return df

def pagina_mapas():
    st.sidebar.header("Opciones a filtrar:") #sidebar lo que nos va a hacer es crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
    df = load_data("NYPD_2018_2023_FELONY_Q.csv")

    #ajuste fecha y hora
    df['CMPLNT_FR_DT'] = pd.to_datetime(df['CMPLNT_FR_DT'], format='%m/%d/%Y')
    df['CMPLNT_FR_TM'] = pd.to_datetime(df['CMPLNT_FR_TM'], format='%H:%M:%S')

    #SELECTORES  

    fecha_inicio_selector_p = st.sidebar.date_input('Fecha de inicio', value=datetime(2023,1,1).date(), key="date1")
    fecha_fin_selector_p = st.sidebar.date_input('Fecha de fin', value=datetime(2023,2,1).date() , key="date2")
    
    #selectores fechas
    fecha_inicio_selector = pd.to_datetime(fecha_inicio_selector_p)
    fecha_fin_selector = pd.to_datetime(fecha_fin_selector_p)

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
    

    # Filtro de fechas
    #filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) & (df['CMPLNT_FR_DT'] <= fecha_fin_selector)]
    
    #filtered_mapa_df = filtered_mapa_df[filtered_mapa_df['OFNS_DESC'].isin(tipo_delito_selector)]
    
    
    ###Aqui es donde pasa la MAGIA. conectar los selectores con la base de datos

    if fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and edad_sosp_selector and raza_sosp_selector and sexo_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and edad_sosp_selector and raza_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and raza_sosp_selector and sexo_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and edad_sosp_selector and sexo_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
        
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and edad_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and sexo_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
        
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector and raza_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                        (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                        (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                        (df['BORO_NM'].isin(municipio_selector)) &
                        (df['SUSP_RACE'].isin(raza_sosp_selector)) 
                        ]  
    ####
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and edad_sosp_selector and raza_sosp_selector and sexo_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]

    elif fecha_inicio_selector and fecha_fin_selector and  tipo_delito_selector and edad_sosp_selector and raza_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and fecha_fin_selector and tipo_delito_selector and edad_sosp_selector and sexo_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector  and raza_sosp_selector and sexo_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector  and edad_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector  and sexo_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
        
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector  and raza_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                        (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                        (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                        (df['SUSP_RACE'].isin(raza_sosp_selector)) 
                        ]  
    
    ####
    elif fecha_inicio_selector and  fecha_fin_selector and municipio_selector and edad_sosp_selector and raza_sosp_selector and sexo_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
        
    elif fecha_inicio_selector and  fecha_fin_selector and  municipio_selector and edad_sosp_selector and raza_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  municipio_selector and edad_sosp_selector and sexo_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  municipio_selector  and raza_sosp_selector and sexo_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_RACE'].isin(raza_sosp_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  municipio_selector  and edad_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_AGE_GROUP'].isin(edad_sosp_selector)) 
                        ]
    
    elif fecha_inicio_selector and  fecha_fin_selector and  municipio_selector  and sexo_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector)) &
                          (df['SUSP_SEX'].isin(sexo_sosp_selector)) 
                        ]
        
    elif fecha_inicio_selector and  fecha_fin_selector and  municipio_selector  and raza_sosp_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                        (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                        (df['BORO_NM'].isin(municipio_selector)) &
                        (df['SUSP_RACE'].isin(raza_sosp_selector)) 
                        ]  
        
    ###
        
    elif fecha_inicio_selector and  fecha_fin_selector and  tipo_delito_selector and municipio_selector: #todos
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector)) &
                          (df['BORO_NM'].isin(municipio_selector))
                        ]
    elif fecha_inicio_selector and fecha_fin_selector and tipo_delito_selector: 
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['OFNS_DESC'].isin(tipo_delito_selector))
                        ]
    elif fecha_inicio_selector and  fecha_fin_selector and municipio_selector: 
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) &
                          (df['CMPLNT_FR_DT'] <= fecha_fin_selector) &
                          (df['BORO_NM'].isin(municipio_selector))
                        ]
    elif  tipo_delito_selector and municipio_selector:
        filtered_mapa_df = df[(df['OFNS_DESC'].isin(tipo_delito_selector)) & 
                         (df['BORO_NM'].isin(municipio_selector)) 
                         ]
    elif fecha_inicio_selector and fecha_fin_selector:
        filtered_mapa_df = df[(df['CMPLNT_FR_DT'] >= fecha_inicio_selector) & (df['CMPLNT_FR_DT'] <= fecha_fin_selector)]
    elif  tipo_delito_selector:
        filtered_mapa_df = df[df['OFNS_DESC'].isin(tipo_delito_selector)]
    elif  municipio_selector:
        filtered_mapa_df = df[df['BORO_NM'].isin(municipio_selector)]
    else:
        filtered_mapa_df = df

    with st.container():
        st.subheader('Ubicación de los crimenes')

        # Seleccione un subconjunto de datos y elimine los valores NaN según el filtro de tipo de delito
        subset_data = filtered_mapa_df.dropna(subset=['Latitude', 'Longitude'])
        # Set sample size to 1000
        sample_size = 1000
        # Determinar un tamaño de muestra que no exceda el tamaño del conjunto de datos disponible.
        sample_size_actual = min(sample_size, len(subset_data))
        if sample_size_actual > 0:
            subset_data_sample = subset_data.sample(sample_size_actual)
            # Obtener los tipos de delitos únicos
            crime_types = subset_data_sample['OFNS_DESC'].unique()
            st.write(crime_types)
            # Definir una lista de colores
            colors = [
                'blue', 'green', 'red', 'purple', 'orange', 'darkblue', 'darkgreen', 'darkred', 
                'lightblue', 'lightgreen', 'lightcoral', 'lightpink', 'gold', 'coral', 'darkorange', 
                'darkviolet', 'salmon', 'skyblue', 'seagreen', 'plum', 'mediumslateblue', 'mediumseagreen', 
                'chocolate', 'firebrick', 'tomato', 'orangered', 'cyan', 'magenta', 'indigo', 'khaki', 
                'mediumturquoise', 'darkslategray', 'yellowgreen', 'steelblue'
            ]
            np.random.shuffle(colors)  # Mezclar los colores

            # Asignar colores aleatorios a cada tipo de delito
            color_map = {crime: colors[i % len(colors)] for i, crime in enumerate(crime_types)}
            
            # Inicializar el mapa usando folio
            m = folium.Map(location=[subset_data_sample['Latitude'].mean(), subset_data_sample['Longitude'].mean()], zoom_start=12)

            #Se agregaron bases al mapa según los filtros de tipo de delito.
            for index, row in subset_data_sample.iterrows():
                crime_type = row['OFNS_DESC']
                # Asegurarse de que el crime_type sea un string para usarlo como clave
                crime_type = str(crime_type)
                folium.CircleMarker(
                    location=[row['Latitude'], row['Longitude']],
                    radius=5,
                    tooltip=crime_type,
                    color=color_map[crime_type],
                    fill=True,
                    fill_color=color_map[crime_type]
                ).add_to(m)

            # Muestra el mapa en Streamlit
            st.markdown("El mapa a continuación muestra las ubicaciones de los delitos según los filtros seleccionados")
            folium_static(m)

        st.subheader('Mapa de calor de deitos')
        if sample_size_actual > 0:
            m_heatmap = folium.Map(location=[subset_data_sample['Latitude'].mean(), subset_data_sample['Longitude'].mean()], zoom_start=12)
            HeatMap(data=subset_data_sample[['Latitude', 'Longitude']].values, radius=10).add_to(m_heatmap)
            folium_static(m_heatmap)
        else:
            st.write("No hay datos disponibles para los filtros seleccionados.")