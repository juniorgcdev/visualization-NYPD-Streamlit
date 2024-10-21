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

def pagina_visualizacion():
    st.title("Pagina visualizacion")
    st.write("Pagina de visualizacion")
    st.sidebar.header('Opciones de filtro viss')

    # Cargar datos
    crime_data = load_data("NYPD_2018_2023_FELONY_Q.csv")

    # Convert to datetime
    crime_data['CMPLNT_FR_DT'] = pd.to_datetime(crime_data['CMPLNT_FR_DT'], errors='coerce')


    
    #st.sidebar.title('Dashboards crímenes de la ciudad de Nueva York')
    st.sidebar.header('Opciones de filtro')

    # Widget filter berdasarkan jenis kejahatan
    selected_crime_type = st.sidebar.selectbox('Seleccionar tipo de crimen', ['All'] + list(crime_data['OFNS_DESC'].unique()))

    # Widget filter berdasarkan rentang tahun
    years = sorted(crime_data['Year'].unique())
    selected_year_range = st.sidebar.slider('Seleccionar rango de año', min_value=int(years[0]), max_value=int(years[-1]), value=(int(years[0]), int(years[-1])))

    # Widget filter berdasarkan borough
    selected_borough = st.sidebar.selectbox('Seleccionar Borough', ['All'] + list(crime_data['BORO_NM'].unique()))

    # Set sample size to 1000
    sample_size = 1000

    # Filtrar datos segun el menú
    if selected_crime_type != 'All':
        crime_type_filter = crime_data['OFNS_DESC'] == selected_crime_type
    else:
        crime_type_filter = pd.Series([True] * len(crime_data))

    year_filter = (crime_data['Year'] >= selected_year_range[0]) & (crime_data['Year'] <= selected_year_range[1])

    if selected_borough != 'All':
        borough_filter = crime_data['BORO_NM'] == selected_borough
    else:
        borough_filter = pd.Series([True] * len(crime_data))

    # Combina todas las condiciones del filtro
    filtered_data = crime_data[crime_type_filter & year_filter & borough_filter]

    # Streamlit layout
    st.title('Dashboards crímenes de la ciudad de Nueva York')


    # Diseño para visualización de población y tipos de delitos.
    col_pop, col_crime = st.columns([1, 1])


    if not filtered_data.empty:
        with col_crime:
            st.subheader('Distribución del tipo de crimen')
            crime_type_counts = filtered_data['OFNS_DESC'].value_counts().nlargest(10).reset_index()
            crime_type_counts.columns = ['Crime Type', 'Number of Crimes']
            fig_crime_type = px.bar(crime_type_counts, x='Number of Crimes', y='Crime Type', title='Top 10 Crime Types', orientation='h', color='Crime Type', color_discrete_sequence=px.colors.sequential.Viridis)
            st.plotly_chart(fig_crime_type)

        #Diseño para visualización de mapas y gráficos.
        col1, col2 = st.columns([1, 1])  # Dividir el diseño en dos columnas.

        # Visualización de mapas de lugares de crimen.
        with col1:
            st.subheader('Crime Locations on Map')

            # Seleccione un subconjunto de datos y elimine los valores NaN según el filtro de tipo de delito
            subset_data = filtered_data.dropna(subset=['Latitude', 'Longitude'])

            # Determinar un tamaño de muestra que no exceda el tamaño del conjunto de datos disponible.
            sample_size_actual = min(sample_size, len(subset_data))
            if sample_size_actual > 0:
                subset_data_sample = subset_data.sample(sample_size_actual)

                # Inicializar el mapa usando folio
                m = folium.Map(location=[subset_data_sample['Latitude'].mean(), subset_data_sample['Longitude'].mean()], zoom_start=12)

                #Se agregaron bases al mapa según los filtros de tipo de delito.
                for index, row in subset_data_sample.iterrows():
                    folium.CircleMarker(
                        location=[row['Latitude'], row['Longitude']],
                        radius=5,
                        tooltip=row['OFNS_DESC'],
                        color='blue',
                        fill=True,
                        fill_color='blue'
                    ).add_to(m)

                # Muestra el mapa en Streamlit
                st.markdown("The map below shows the locations of crimes based on the selected filters.")
                folium_static(m)

        #Visualización de la delincuencia por municipio a lo largo del tiempo utilizando Altair
        with col2:
            st.subheader('Tendencias delictivas por municipio')
            chart_type = st.selectbox('Select Chart Type', ['Bar Chart', 'Line Chart'], key='chart_type')

            # Agrupamiento por barrio y año, usando .size() para contar los registros
            crime_borough_yearly = filtered_data.groupby(['BORO_NM', filtered_data['CMPLNT_FR_DT'].dt.year]).size().reset_index(name='TOTAL_CRIMES')

            # Crear el gráfico según el tipo seleccionado
            fig_borough_yearly = (
                px.bar(crime_borough_yearly, x='CMPLNT_FR_DT', y='TOTAL_CRIMES', color='BORO_NM', title='Crime Trends by Borough')
                if chart_type == 'Bar Chart'
                else px.line(crime_borough_yearly, x='CMPLNT_FR_DT', y='TOTAL_CRIMES', color='BORO_NM', title='Crime Trends by Borough', markers=True)
            )
            st.plotly_chart(fig_borough_yearly)

        #Visualización del crimen por municipio
        col3, col4 = st.columns([1, 1])

        # Agregue un gráfico circular en Tendencias criminales por distrito
        with col3:
            st.subheader('Porcentaje de criminalidad por municipio')
            crime_borough_counts = filtered_data['BORO_NM'].value_counts().reset_index()
            crime_borough_counts.columns = ['Borough', 'Number of Crimes']

            fig_pie = px.pie(crime_borough_counts, values='Number of Crimes', names='Borough', title='Crime Percentage by Borough', color_discrete_sequence=px.colors.sequential.Viridis)
            st.plotly_chart(fig_pie)

        # Visualización del mapa de calor del crimen
        with col4:
            st.subheader('Crime Heatmap')
            if sample_size_actual > 0:
                m_heatmap = folium.Map(location=[subset_data_sample['Latitude'].mean(), subset_data_sample['Longitude'].mean()], zoom_start=12)
                HeatMap(data=subset_data_sample[['Latitude', 'Longitude']].values, radius=10).add_to(m_heatmap)
                folium_static(m_heatmap)
            else:
                st.write("No hay datos disponibles para los filtros seleccionados.")

    else:
        st.write("Seleccione al menos una opción de filtro de la barra lateral para mostrar datos")


