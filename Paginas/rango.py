import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
#from folium.plugins import HeatMap
from datetime import datetime
import altair as alt
import numpy as np
from folium.plugins import MarkerCluster
from streamlit.components.v1 import html

@st.cache_data()
def load_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    select_columnas = ['Year', 'OFNS_DESC','CMPLNT_FR_DT','CMPLNT_FR_TM','BORO_NM','SUSP_AGE_GROUP','SUSP_RACE','SUSP_SEX','VIC_AGE_GROUP','VIC_RACE','VIC_SEX','Latitude','Longitude']
    df = df[select_columnas]
    df = df[df['OFNS_DESC'] != '(null)']
    return df


def pagina_rango():

    st.sidebar.header("Opciones a filtrar:") #sidebar lo que nos va a hacer es crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
    df = load_data("NYPD_2018_2023_FELONY_Q.csv")

    #ajuste fecha y hora
    df['CMPLNT_FR_DT'] = pd.to_datetime(df['CMPLNT_FR_DT'], format='%m/%d/%Y')
    df['CMPLNT_FR_TM'] = pd.to_datetime(df['CMPLNT_FR_TM'], format='%H:%M:%S')
    '''
    df['CMPLNT_FR_DT'] = pd.to_datetime(df['CMPLNT_FR_DT'], format='%m/%d/%Y')
    df['CMPLNT_FR_TM'] = pd.to_datetime(df['CMPLNT_FR_TM'], format='%H:%M:%S').dt.strftime('%H:%M:%S')
    '''
    #SELECTORES  

    fecha_inicio_selector_p = st.sidebar.date_input('Fecha de inicio', value=datetime(2023,1,1).date(), key="date1")
    fecha_fin_selector_p = st.sidebar.date_input('Fecha de fin', value=datetime(2023,5,20).date() , key="date2")
    
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
    # Inyectar CSS para ocultar el widget
    hide_multiselect_css = """
    <style>
    .hidden-multiselect {
        display: none;
    }
    </style>
    """

    html(hide_multiselect_css, height=0)
    
    # Filtrar por edad sospechoso seleccionados
    edad_sosp_selector = st.sidebar.multiselect(
        "Seleccione edad sospechoso:",
        options = df['SUSP_AGE_GROUP'].unique(),
        key="multiselect1"
    )

    # Filtrar por raza sospechoso seleccionados
    raza_sosp_selector = st.sidebar.multiselect(
        "Seleccione raza sospechoso:",
        options = df['SUSP_RACE'].unique(),
        key="multiselect2"
    )

    # Filtrar sexo sospechoso seleccionados
    sexo_sosp_selector = st.sidebar.multiselect(
        "Seleccione un sexo Sospechoso:",
        options = df['SUSP_SEX'].unique(),
        key="multiselect3"
    )

    html('<div class="hidden-multiselect" id="multiselect1"></div>', height=0)
    html('<div class="hidden-multiselect" id="multiselect2"></div>', height=0)
    html('<div class="hidden-multiselect" id="multiselect3"></div>', height=0)


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
        ######container pagina principal##############
    
        left_column , right_column = st.columns([2,4])

        with left_column:
            st.subheader('Ranking')
            anio_delito_df = filtered_df[['Year','OFNS_DESC']]
            count_anio_delito_df = anio_delito_df.groupby('OFNS_DESC').size().reset_index(name='contador')
            count_anio_delito_sorted_df= count_anio_delito_df.sort_values(by="contador", ascending=False)
            # Definir una función para truncar cadenas
            def truncate_text(text, length=15):
                if len(text) > length:
                    return text[:length] + '...'
                return text
            # Aplicar la función de truncamiento a la columna 'Texto'
            count_anio_delito_sorted_df['OFNS_DESC_TRUNC'] = count_anio_delito_sorted_df['OFNS_DESC'].apply(lambda x: truncate_text(x, length=15))
            # Opción 1: Mostrar datos con formateo manual de columnas
            
            st.dataframe(count_anio_delito_sorted_df,
                    column_order=("OFNS_DESC_TRUNC", "contador"),
                    hide_index=True,
                    width=None,
                    column_config={
                        "OFNS_DESC_TRUNC": st.column_config.TextColumn(
                            "Delito",
                        ),
                        "contador": st.column_config.ProgressColumn(
                            "Cantidad",
                            format="%f",
                            min_value=0,
                            max_value=max(count_anio_delito_sorted_df.contador),
                        )}
                    )
            
        
        with right_column:
            st.subheader('Mapa de delitos')
            # Seleccione un subconjunto de datos y elimine los valores NaN según el filtro de tipo de delito
            subset_data = filtered_df.dropna(subset=['Latitude', 'Longitude'])
            # Set sample size to 1000
            sample_size = 1000
            # Determinar un tamaño de muestra que no exceda el tamaño del conjunto de datos disponible.
            sample_size_actual = min(sample_size, len(subset_data))
            if sample_size_actual > 0:
                subset_data_sample = subset_data.sample(sample_size_actual)
                # Obtener los tipos de delitos únicos
                crime_types = subset_data_sample['OFNS_DESC'].unique()
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
                m = folium.Map(location=[subset_data_sample['Latitude'].mean(), subset_data_sample['Longitude'].mean()], zoom_start=11)

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
                folium_static(m,width=550, height=450)

            
        
        ##################################
        left_column_meses ,center_column_meses, right_column_meses = st.columns([0.5,8,0.5])
        with center_column_meses:
            line_chart_df = filtered_df
            line_chart_df['Month'] = line_chart_df['CMPLNT_FR_DT'].dt.month
            line_chart_df['Year'] = line_chart_df['CMPLNT_FR_DT'].dt.year
            line_chart_df['Hour'] = line_chart_df['CMPLNT_FR_TM'].dt.hour.astype(str)

            # Crear una columna combinada para la visualización
            line_chart_df['Month_Year'] = line_chart_df['CMPLNT_FR_DT'].dt.to_period('M').astype(str)

            # Filtrar el dataframe por los delitos seleccionados
            if tipo_delito_selector:
                df_filtrado = line_chart_df[line_chart_df['OFNS_DESC'].isin(tipo_delito_selector)]
            else:
                df_filtrado = line_chart_df[line_chart_df['OFNS_DESC'].isin(df['OFNS_DESC'].unique())]

            # Agrupar por mes y año, y contar la cantidad de delitos
            df_agrupado = df_filtrado.groupby(['Month', 'OFNS_DESC']).size().reset_index(name='Count')
        
            # Crear una lista completa de meses para asegurarse de que todos los meses del año estén presentes en el eje X
            '''
            todos_los_meses = pd.date_range(start=df_agrupado['Month_Year'].min(), 
                                    end=df_agrupado['Month_Year'].max(), 
                                    freq='MS').strftime('%Y-%m').tolist()
            '''
            fig2 = px.line(df_agrupado, x='Month', y='Count', color='OFNS_DESC', title='Tendencia en los meses del año', markers=True)
            #fig2.update_xaxes(type='category', tickmode='array', tickvals=todos_los_meses, ticktext=[pd.to_datetime(m, format='%Y-%m').strftime('%b %Y') for m in todos_los_meses])
            fig2.update_xaxes(
                tickmode='array',
                tickvals=df_agrupado['Month'].unique(),
                ticktext=df_agrupado['Month'].unique()
            )
            st.plotly_chart(fig2, use_container_width=True)
            
        ###################################
        left_column_susp ,center_column_susp, right_column_susp = st.columns([2,2,2])

        #count_susp_age_df= count_susp_age_df.sort_values(by="cantidad", ascending=False)
        with left_column_susp:
            count_susp_age_df = filtered_df[['SUSP_AGE_GROUP']]
            count_susp_age_df = count_susp_age_df.groupby('SUSP_AGE_GROUP').size().reset_index(name='cantidad')
            count_susp_age_df.columns = ['Edad_Sospechoso', 'cantidad']
            fig_susp_age_df = px.pie(count_susp_age_df, values='cantidad', names='Edad_Sospechoso', title='Porcentaje por Edad del Sospechoso', color_discrete_sequence=px.colors.sequential.Viridis)
            st.plotly_chart(fig_susp_age_df)
        with center_column_susp:
            count_susp_race_df = filtered_df[['SUSP_RACE']]
            count_susp_race_df = count_susp_race_df.groupby('SUSP_RACE').size().reset_index(name='cantidad')
            count_susp_race_df.columns = ['Raza_Sospechoso', 'cantidad']
            fig_susp_race_df = px.pie(count_susp_race_df, values='cantidad', names='Raza_Sospechoso', title='Porcentaje por Raza del Sospechoso', color_discrete_sequence=px.colors.sequential.Plasma)
            st.plotly_chart(fig_susp_race_df)
        with right_column_susp:
            count_susp_sex_df = filtered_df[['SUSP_SEX']]
            count_susp_sex_df = count_susp_sex_df.groupby('SUSP_SEX').size().reset_index(name='cantidad')
            count_susp_sex_df.columns = ['Sexo_Sospechoso', 'cantidad']
            fig_susp_sex_df = px.pie(count_susp_sex_df, values='cantidad', names='Sexo_Sospechoso', title='Porcentaje por Sexo del Sospechoso', color_discrete_sequence=px.colors.sequential.Magma)
            st.plotly_chart(fig_susp_sex_df)
        

        ##########################################
        left_column_hora ,center_column_hora, right_column_hora = st.columns([0.5,8,0.5])
        with center_column_hora:
            # Agrupar por mes y año, y contar la cantidad de delitos
            df_agrupado_hora = df_filtrado.groupby(['Hour', 'OFNS_DESC']).size().reset_index(name='Count')
            df_agrupado_hora['Hour'] = df_agrupado_hora['Hour'].astype(int)
            df_agrupado_hora = df_agrupado_hora.sort_values(by='Hour')
            fig4 = px.line(df_agrupado_hora, x='Hour', y='Count', color='OFNS_DESC', title='Tendencia en las horas', markers=True)
            fig4.update_xaxes(
                tickmode='array',
                tickvals=df_agrupado_hora['Hour'].unique(),
                ticktext=df_agrupado_hora['Hour'].unique()
            )
            st.plotly_chart(fig4, use_container_width=True)

        ###########################################
        left_column_vic ,center_column_vic, right_column_vic = st.columns([2,2,2])

        with left_column_vic:
            count_vic_age_df = filtered_df[['VIC_AGE_GROUP']]
            count_vic_age_df = count_vic_age_df.groupby('VIC_AGE_GROUP').size().reset_index(name='cantidad')
            count_vic_age_df.columns = ['Edad_Victima', 'cantidad']
            fig_vic_age_df = px.pie(count_vic_age_df, values='cantidad', names='Edad_Victima', title='Porcentaje por Edad del Victima', color_discrete_sequence=px.colors.sequential.Inferno)
            st.plotly_chart(fig_vic_age_df)
        with center_column_vic:
            count_vic_race_df = filtered_df[['VIC_RACE']]
            count_vic_race_df = count_vic_race_df.groupby('VIC_RACE').size().reset_index(name='cantidad')
            count_vic_race_df.columns = ['Raza_Victima', 'cantidad']
            fig_vic_race_df = px.pie(count_vic_race_df, values='cantidad', names='Raza_Victima', title='Porcentaje por Raza del Victima', color_discrete_sequence=px.colors.sequential.Cividis)
            st.plotly_chart(fig_vic_race_df)
        with right_column_vic:
            count_vic_sex_df = filtered_df[['VIC_SEX']]
            count_vic_sex_df = count_vic_sex_df.groupby('VIC_SEX').size().reset_index(name='cantidad')
            count_vic_sex_df.columns = ['Sexo_Victima', 'cantidad']
            fig_vic_sex_df = px.pie(count_vic_sex_df, values='cantidad', names='Sexo_Victima', title='Porcentaje por Sexo del Victima', color_discrete_sequence=px.colors.sequential.Plotly3)
            st.plotly_chart(fig_vic_sex_df)
        
        st.divider()

        delitos_tipo_municipio = df_filtrado.groupby(['OFNS_DESC', 'BORO_NM']).size().reset_index(name='Total Delitos')
        fig = px.bar(delitos_tipo_municipio, x='OFNS_DESC', y='Total Delitos', color='BORO_NM', barmode='stack',
                    title='Número de Delitos por  Municipio')
        st.plotly_chart(fig)


        df_filtrado['Hora'] = pd.to_datetime(df_filtrado['CMPLNT_FR_TM'], format='%H:%M').dt.hour
        delitos_hora_tipo = df_filtrado.groupby(['Hora', 'OFNS_DESC']).size().reset_index(name='Total Delitos')
        fig = px.line(delitos_hora_tipo, x='Hora', y='Total Delitos', color='OFNS_DESC', markers=True,
                    title='Número de Delitos por Hora del Día ')
        st.plotly_chart(fig)


        delitos_edad_sospechoso_tipo = df_filtrado.groupby(['SUSP_AGE_GROUP', 'OFNS_DESC']).size().reset_index(name='Total Delitos')
        fig = px.bar(delitos_edad_sospechoso_tipo, x='SUSP_AGE_GROUP', y='Total Delitos', color='OFNS_DESC', barmode='stack',
                    title='Número de Delitos por Edad del Sospechoso')
        st.plotly_chart(fig)


        delitos_raza_sospechoso_tipo = df_filtrado.groupby(['SUSP_RACE', 'OFNS_DESC']).size().reset_index(name='Total Delitos')
        fig = px.bar(delitos_raza_sospechoso_tipo, x='SUSP_RACE', y='Total Delitos', color='OFNS_DESC', barmode='stack',
                    title='Número de Delitos por Raza del Sospechoso')
        st.plotly_chart(fig)


        delitos_sexo_sospechoso_tipo = df_filtrado.groupby(['SUSP_SEX', 'OFNS_DESC']).size().reset_index(name='Total Delitos')
        fig = px.bar(delitos_sexo_sospechoso_tipo, x='SUSP_SEX', y='Total Delitos', color='OFNS_DESC', barmode='stack',
                    title='Número de Delitos por Sexo del Sospechoso ')
        st.plotly_chart(fig)
