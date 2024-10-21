import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import numpy as np
import altair as alt

@st.cache_data()
def load_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    select_columnas = ['Year', 'OFNS_DESC','CMPLNT_FR_DT','CMPLNT_FR_TM','BORO_NM','SUSP_AGE_GROUP','SUSP_RACE','SUSP_SEX','VIC_AGE_GROUP','VIC_RACE','VIC_SEX','Latitude','Longitude']
    df = df[select_columnas]
    df = df[df['OFNS_DESC'] != '(null)']
    return df

def pagina_principal():
    df = load_data("NYPD_2018_2023_FELONY_Q.csv")
    #ajuste fecha y hora
    df['CMPLNT_FR_DT'] = pd.to_datetime(df['CMPLNT_FR_DT'], format='%m/%d/%Y')
    df['CMPLNT_FR_TM'] = pd.to_datetime(df['CMPLNT_FR_TM'], format='%H:%M:%S')

    #Filtros del sidebar
    detalle_delito_selector = st.sidebar.multiselect(
        "Seleccione un delito:",
        options = df['OFNS_DESC'].unique()
    )

    #Condiciones según el filtro
    if  detalle_delito_selector:
        df_seleccion = df[df['OFNS_DESC'].isin(detalle_delito_selector)]

    else:
        df_seleccion = df
    ###################################MAIN###############################################################
    
    #########################################Bloque 1##########################################################
    #lo ponemos en otro dataframe
    line_chart_anios_df = df_seleccion
    left_column_a , right_column_a = st.columns([5,2])
    with left_column_a:
        st.subheader('Mapa de delitos')
        # Seleccione un subconjunto de datos y elimine los valores NaN según el filtro de tipo de delito
        subset_data = df_seleccion.dropna(subset=['Latitude', 'Longitude'])
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
            st.markdown("Ubicaciones de los delitos")
            folium_static(m,width=500, height=400)

        
    with right_column_a:
        st.subheader("Tabla de delitos por año")
        delitos_anio_g_df = pd.crosstab(index=line_chart_anios_df['Year'].astype(str), columns=line_chart_anios_df['OFNS_DESC'])
        if not detalle_delito_selector:
            all_columns = line_chart_anios_df['OFNS_DESC'].unique()
        else:
            all_columns = detalle_delito_selector
        delitos_anio_g_df = delitos_anio_g_df.reindex(columns=all_columns, fill_value=0)
        delitos_anio_g_df.index.name = 'Año'
        delitos_anio_g_df = delitos_anio_g_df.reset_index()
        st.dataframe(delitos_anio_g_df)

        
    #############################################Bloque 2#########################################################
    # Realizar el conteo de ocurrencias
    st.subheader("Tendencia de delitos por año")

    # Filtrar el dataframe por los delitos seleccionados
    if detalle_delito_selector:
        filtrado_chart_anios_df = line_chart_anios_df[line_chart_anios_df['OFNS_DESC'].isin(detalle_delito_selector)]
    else:
        filtrado_chart_anios_df = line_chart_anios_df[line_chart_anios_df['OFNS_DESC'].isin(df['OFNS_DESC'].unique())]

    # Agrupar por mes y año, y contar la cantidad de delitos
    agrupado_chart_anios_df = filtrado_chart_anios_df.groupby(['Year', 'OFNS_DESC']).size().reset_index(name='Count')
    # Crear una lista completa de meses para asegurarse de que todos los meses del año estén presentes en el eje X
    '''
    todos_los_meses = pd.date_range(start=df_agrupado['Month_Year'].min(), 
                            end=df_agrupado['Month_Year'].max(), 
                            freq='MS').strftime('%Y-%m').tolist()
    '''
    fig2 = px.line(agrupado_chart_anios_df, x='Year', y='Count', color='OFNS_DESC', title='', markers=True)
    #fig2.update_xaxes(type='category', tickmode='array', tickvals=todos_los_meses, ticktext=[pd.to_datetime(m, format='%Y-%m').strftime('%b %Y') for m in todos_los_meses])
    fig2.update_xaxes(
        tickmode='array',
        tickvals=agrupado_chart_anios_df['Year'].unique(),
        ticktext=agrupado_chart_anios_df['Year'].unique()
    )
    st.plotly_chart(fig2, use_container_width=True)
    ###################################Tabsss##############################################
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Número de Delitos por Municipio, Año y Tipo de Delito",
                                             "Delitos por Raza del Sospechoso, Año y Tipo de Delito",
                                               "Delitos por Edad del Sospechoso, Año y Tipo de Delito",
                                               "Delitos por Raza del Sospechoso, Año y Tipo de Delito",
                                               "Distribución de Delitos por Hora del Día, Año y Tipo de Delito"])
    with tab1:
        st.subheader("Número de Delitos por Municipio, Año y Tipo de Delito")
        delitos_municipio_anio_tipo = filtrado_chart_anios_df.groupby(['Year', 'BORO_NM', 'OFNS_DESC']).size().reset_index(name='Total Delitos')
        fig = px.bar(delitos_municipio_anio_tipo, x='Year', y='Total Delitos', color='OFNS_DESC', facet_col='BORO_NM',
                    barmode='stack', title='Número de Delitos por Municipio, Año y Tipo de Delito')
        st.plotly_chart(fig)
    with tab2:
        st.subheader("Delitos por Sexo del Sospechoso, Año y Tipo de Delito")
        delitos_sexo_sospechoso_anio_tipo = filtrado_chart_anios_df.groupby(['Year', 'SUSP_SEX', 'OFNS_DESC']).size().reset_index(name='Total Delitos')
        fig = px.bar(delitos_sexo_sospechoso_anio_tipo, x='Year', y='Total Delitos', color='OFNS_DESC', facet_col='SUSP_SEX',
                    barmode='stack', title='Número de Delitos por Sexo del Sospechoso, Año y Tipo de Delito')
        st.plotly_chart(fig) 
    with tab3:
        st.subheader("Delitos por Edad del Sospechoso, Año y Tipo de Delito")
        delitos_edad_sospechoso_anio_tipo = filtrado_chart_anios_df.groupby(['Year', 'SUSP_AGE_GROUP', 'OFNS_DESC']).size().reset_index(name='Total Delitos')
        fig = px.bar(delitos_edad_sospechoso_anio_tipo, x='Year', y='Total Delitos', color='OFNS_DESC', facet_col='SUSP_AGE_GROUP',
                    barmode='stack', title='Número de Delitos por Edad del Sospechoso, Año y Tipo de Delito')
        st.plotly_chart(fig)
    with tab4:
        st.subheader("Delitos por Raza del Sospechoso, Año y Tipo de Delito")
        delitos_raza_sospechoso_anio_tipo = filtrado_chart_anios_df.groupby(['Year', 'SUSP_RACE', 'OFNS_DESC']).size().reset_index(name='Total Delitos')
        fig = px.bar(delitos_raza_sospechoso_anio_tipo, x='Year', y='Total Delitos', color='OFNS_DESC', facet_col='SUSP_RACE',
                    barmode='stack', title='Número de Delitos por Raza del Sospechoso, Año y Tipo de Delito')
        st.plotly_chart(fig)
    with tab5:
        st.subheader("Distribución de Delitos por Hora del Día, Año y Tipo de Delito")
        filtrado_chart_anios_df['Hora'] = pd.to_datetime(filtrado_chart_anios_df['CMPLNT_FR_TM'], format='%H:%M').dt.hour
        delitos_hora_anio_tipo = filtrado_chart_anios_df.groupby(['Year', 'Hora', 'OFNS_DESC']).size().reset_index(name='Total Delitos')
        fig = px.line(delitos_hora_anio_tipo, x='Hora', y='Total Delitos', color='OFNS_DESC', facet_col='Year',
                    markers=True, title='Número de Delitos por Hora del Día, Año y Tipo de Delito')
        st.plotly_chart(fig)
    ###########################################################################################
    st.subheader("Acumulados de todos los periodos")
    ###############################Bloque de sospechoso######################################
    left_column_susp ,center_column_susp, right_column_susp = st.columns([2,2,2])

    #count_susp_age_df= count_susp_age_df.sort_values(by="cantidad", ascending=False)
    with left_column_susp:
        count_susp_age_df = df_seleccion[['SUSP_AGE_GROUP']]
        count_susp_age_df = count_susp_age_df.groupby('SUSP_AGE_GROUP').size().reset_index(name='cantidad')
        count_susp_age_df.columns = ['Edad_Sospechoso', 'cantidad']
        fig_susp_age_df = px.pie(count_susp_age_df, values='cantidad', names='Edad_Sospechoso', title='Porcentaje por Edad del Sospechoso', color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig_susp_age_df)
    with center_column_susp:
        count_susp_race_df = df_seleccion[['SUSP_RACE']]
        count_susp_race_df = count_susp_race_df.groupby('SUSP_RACE').size().reset_index(name='cantidad')
        count_susp_race_df.columns = ['Raza_Sospechoso', 'cantidad']
        fig_susp_race_df = px.pie(count_susp_race_df, values='cantidad', names='Raza_Sospechoso', title='Porcentaje por Raza del Sospechoso', color_discrete_sequence=px.colors.sequential.Plasma)
        st.plotly_chart(fig_susp_race_df)
    with right_column_susp:
        count_susp_sex_df = df_seleccion[['SUSP_SEX']]
        count_susp_sex_df = count_susp_sex_df.groupby('SUSP_SEX').size().reset_index(name='cantidad')
        count_susp_sex_df.columns = ['Sexo_Sospechoso', 'cantidad']
        fig_susp_sex_df = px.pie(count_susp_sex_df, values='cantidad', names='Sexo_Sospechoso', title='Porcentaje por Sexo del Sospechoso', color_discrete_sequence=px.colors.sequential.Magma)
        st.plotly_chart(fig_susp_sex_df)
    #############################################################################################
    line_chart_df = df_seleccion
    line_chart_df['Month'] = line_chart_df['CMPLNT_FR_DT'].dt.month
    line_chart_df['Year'] = line_chart_df['CMPLNT_FR_DT'].dt.year
    line_chart_df['Hour'] = line_chart_df['CMPLNT_FR_TM'].dt.hour.astype(str)

    # Crear una columna combinada para la visualización
    line_chart_df['Month_Year'] = line_chart_df['CMPLNT_FR_DT'].dt.to_period('M').astype(str)

    # Filtrar el dataframe por los delitos seleccionados
    if detalle_delito_selector:
        df_filtrado = line_chart_df[line_chart_df['OFNS_DESC'].isin(detalle_delito_selector)]
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
    ########################################Bloque de victimass################################
    left_column_vic ,center_column_vic, right_column_vic = st.columns([2,2,2])

    with left_column_vic:
        count_vic_age_df = df_seleccion[['VIC_AGE_GROUP']]
        count_vic_age_df = count_vic_age_df.groupby('VIC_AGE_GROUP').size().reset_index(name='cantidad')
        count_vic_age_df.columns = ['Edad_Victima', 'cantidad']
        fig_vic_age_df = px.pie(count_vic_age_df, values='cantidad', names='Edad_Victima', title='Porcentaje por Edad del Victima', color_discrete_sequence=px.colors.sequential.Inferno)
        st.plotly_chart(fig_vic_age_df)
    with center_column_vic:
        count_vic_race_df = df_seleccion[['VIC_RACE']]
        count_vic_race_df = count_vic_race_df.groupby('VIC_RACE').size().reset_index(name='cantidad')
        count_vic_race_df.columns = ['Raza_Victima', 'cantidad']
        fig_vic_race_df = px.pie(count_vic_race_df, values='cantidad', names='Raza_Victima', title='Porcentaje por Raza del Victima', color_discrete_sequence=px.colors.sequential.Cividis)
        st.plotly_chart(fig_vic_race_df)
    with right_column_vic:
        count_vic_sex_df = df_seleccion[['VIC_SEX']]
        count_vic_sex_df = count_vic_sex_df.groupby('VIC_SEX').size().reset_index(name='cantidad')
        count_vic_sex_df.columns = ['Sexo_Victima', 'cantidad']
        fig_vic_sex_df = px.pie(count_vic_sex_df, values='cantidad', names='Sexo_Victima', title='Porcentaje por Sexo del Victima', color_discrete_sequence=px.colors.sequential.Plotly3)
        st.plotly_chart(fig_vic_sex_df)
  
    #########################################Bloque 3##############################################
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
   
