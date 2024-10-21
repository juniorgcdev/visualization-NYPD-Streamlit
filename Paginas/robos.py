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

@st.cache_data()
def load_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    return df


def pagina_robos():
    st.title("Pagina Principal")
    st.write("Pagina de Principal")
    st.sidebar.header("Opciones a filtrar:") #sidebar lo que nos va a hacer es crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
    df = load_data("NYPD_2018_2023_FELONY_Q.csv")

    sorted_years = sorted(df['Year'].unique())
    first_two_years = sorted_years[:2]
    anio_selector = st.sidebar.multiselect(
        "Seleccione el año:",
        options = df['Year'].unique(),
        default = first_two_years
    )
    
    detalle_delito = st.sidebar.multiselect(
        "Seleccione la descripción:",
        options = df['OFNS_DESC'].unique()
    )
    
    tipo_delito = ['FELONY']
    
    ###Aqui es donde pasa la MAGIA. conectar los selectores con la base de datos
    if anio_selector  and  detalle_delito:
        df_seleccion = df[df['Year'].isin(anio_selector) & df['OFNS_DESC'].isin(detalle_delito)]
    elif anio_selector :
        df_seleccion = df[df['Year'].isin(anio_selector) ]
    elif  anio_selector and detalle_delito:
        df_seleccion = df[df['Year'].isin(anio_selector) & df['OFNS_DESC'].isin(detalle_delito)]
    elif  detalle_delito:
        df_seleccion = df[df['OFNS_DESC'].isin(detalle_delito) ]
    else:
        df_seleccion = df

    
    with st.container():
        st.write("This is inside the container")
        
        total_anio = int(df_seleccion['Year'].count())

        #total_delito = int(df_seleccion['LAW_CAT_CD'].count())


        st.subheader('Total por delito:')
        robbery_df = df_seleccion[df_seleccion['OFNS_DESC'] == 'ROBBERY']

        # Agrupar por año y grupo de edad del sospechoso, y contar la frecuencia de robos
        age_group_counts = robbery_df.groupby(['Year', 'SUSP_RACE']).size().unstack(fill_value=0)

        # Título de la aplicación
        st.title('Evolución Temporal de la Edad de los Sospechosos en Robos (2018-2023)')

        # Crear el gráfico de líneas para visualizar la tendencia a lo largo del tiempo
        fig, ax = plt.subplots(figsize=(12, 6))
        for age_group in age_group_counts.columns:
            ax.plot(age_group_counts.index, age_group_counts[age_group], marker='o', label=age_group)

        ax.set_title('Evolución Temporal de la Edad de los Sospechosos en Robos (2018-2023)')
        ax.set_xlabel('Año')
        ax.set_ylabel('Número de Robos')
        ax.legend(title='Grupo de Edad del Sospechoso')
        ax.grid(True)

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)


        st.write("This is outside the container")
        st.write("OTRO GRAFIC")
        
        df['CMPLNT_FR_DT'] = pd.to_datetime(df['CMPLNT_FR_DT'], format='%m/%d/%Y')
        # Contar los incidentes por hora y tipo de incidente
        def get_incident_counts(filtered_df):
            return filtered_df.groupby(['CMPLNT_FR_TM', 'OFNS_DESC']).size().unstack(fill_value=0)

        # Función para generar la gráfica
        def plot_incidents(selected_incidents, filtered_df):
            incident_counts = get_incident_counts(filtered_df)
            fig = go.Figure()
            
            for incident in selected_incidents:
                if incident in incident_counts.columns:
                    fig.add_trace(go.Scatter(
                        x=incident_counts.index,
                        y=incident_counts[incident],
                        mode='lines+markers',
                        name=incident,
                        text=incident_counts[incident],
                        textposition='top center'
                    ))
            
            fig.update_layout(
                title='Número de Incidentes por Hora',
                xaxis_title='Hora del Día',
                yaxis_title='Número de Incidentes',
                xaxis=dict(tickvals=list(range(24)), ticktext=[f'{i}:00' for i in range(24)]),
                yaxis=dict(title='Cantidad de Incidentes'),
                hovermode='closest'
            )
            
            return fig

        # Interfaz de usuario de Streamlit
        st.title('Análisis de Incidentes de NYPD')

        # Selector de fechas
        start_date = st.date_input('Fecha de Inicio', min(df['CMPLNT_FR_DT']), min(df['CMPLNT_FR_DT']), max(df['CMPLNT_FR_DT']))
        end_date = st.date_input('Fecha de Fin', min(df['CMPLNT_FR_DT']), min(df['CMPLNT_FR_DT']), max(df['CMPLNT_FR_DT']))

        if start_date > end_date:
            st.error('La fecha de inicio no puede ser mayor que la fecha de fin.')
        else:
            # Filtrar el DataFrame por el rango de fechas
            filtered_df = df[(df['CMPLNT_FR_DT'] >= pd.to_datetime(start_date)) & (df['CMPLNT_FR_DT'] <= pd.to_datetime(end_date))]
            
            # Selector de tipos de incidentes
            incident_types = filtered_df['OFNS_DESC'].unique()
            selected_incidents = st.multiselect('Selecciona los tipos de incidentes:', incident_types)
            
            if selected_incidents:
                # Crear el gráfico con los incidentes seleccionados
                fig = plot_incidents(selected_incidents, filtered_df)
                st.plotly_chart(fig)
            else:
                st.write('Selecciona al menos un tipo de incidente para mostrar la gráfica.')



