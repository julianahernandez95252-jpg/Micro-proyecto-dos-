import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

# configuración de la página
st.set_page_config(page_title="Top mejores Series", 
                   layout="wide", 
                   page_icon="📽")

#---Backround
st.image("https://github.com/julianahernandez95252-jpg/Micro-proyecto-dos-/blob/main/imdb.jpg?raw=true",use_container_width=True)

#---Titulo de la aplicacion
st.title("🎬 Análisis de las Mejores Series de IMDb (Top 2000)")

ruta = "data\\mis_datos_descargados.csv"
df =  pd.read_csv(ruta) 

# BLOQUE DE FILTROS (BARRA LATERAL / SIDEBAR)
st.sidebar.header("FILTROS")

# 1. Filtro de Género
generos_disponibles = sorted(df['genres'].dropna().unique())
generos_seleccionados = st.sidebar.multiselect(
    "GÉNERO", 
    options=generos_disponibles, 
    default=generos_disponibles
)

# 2. Filtro de Años (Usa la columna 'start' para el rango de lanzamiento)
año_min = int(df['startYear'].dropna().min())
año_max = int(df['startYear'].dropna().max())
años_seleccionados = st.sidebar.slider(
    "AÑOS", 
    min_value=año_min, 
    max_value=año_max, 
    value=(año_min, año_max)
)

# 3. Filtro de Puntuación
puntuacion_seleccionada = st.sidebar.slider(
    "PUNTUACIÓN", 
    min_value=1.0, 
    max_value=10.0, 
    value=(float(df['averageRating'].min()), float(df['averageRating'].max())),
    step=0.1
)

# 4. Filtro de Votos
votos_min, votos_max = int(df['numVotes'].min()), int(df['numVotes'].max())
votos_seleccionados = st.sidebar.slider(
    "VOTOS", 
    min_value=votos_min, 
    max_value=votos_max, 
    value=(votos_min, votos_max)
)

# --- APLICACIÓN DE LOS FILTROS AL DATAFRAME ---
df_filtrado = df[
    (df['genres'].isin(generos_seleccionados)) &
    (df['startYear'].between(años_seleccionados[0], años_seleccionados[1])) &
    (df['averageRating'].between(puntuacion_seleccionada[0], puntuacion_seleccionada[1])) &
    (df['numVotes'].between(votos_seleccionados[0], votos_seleccionados[1]))
]

# CONTENIDO PRINCIPAL (DERECHA DEL PANEL)

if not df_filtrado.empty:
    
    # FILA 1: TARJETAS / KPIS (4 Columnas)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="TOTAL SERIES", value=f"{len(df_filtrado)}")
        
    with col2:
        promedio_punt = df_filtrado['averageRating'].mean().round(1)
        st.metric(label="PROMEDIO PUNTUACIÓN", value=f"{promedio_punt} ⭐")
        
    with col3:
        mejor_serie = df_filtrado.loc[df_filtrado['averageRating'].idxmax()]['primaryTitle']
        if len(str(mejor_serie)) > 20:
            mejor_serie = str(mejor_serie)[:18] + "..."
        st.metric(label="SERIE MEJOR VALORADA", value=mejor_serie)
        
    with col4:
        genero_top = df_filtrado['genres'].mode()[0]
        st.metric(label="GÉNERO MÁS POPULAR", value=genero_top)
        
    st.divider()

    # FILA 2: DISTRIBUCIONES (3 Columnas)
    col_g1, col_g2, col_g3 = st.columns(3)
    
    with col_g1:
        st.subheader("DISTRIBUCIÓN POR GÉNERO")
        conteo_genero = df_filtrado['genres'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.bar(conteo_genero.index, conteo_genero.values, color="#934790")
        ax1.set_ylabel("Cantidad")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig1)
        
    with col_g2:
        st.subheader("DISTRIBUCIÓN DE PUNTUACIONES")
        fig2 = px.histogram(df_filtrado, x="averageRating", nbins=15, 
                             color_discrete_sequence=['#4B4B4B'])
        fig2.update_layout(showlegend=False, yaxis_title="Frecuencia", xaxis_title="Nota IMDb")
        st.plotly_chart(fig2, use_container_width=True)
        
    with col_g3:
        st.subheader("SERIES POR AÑO DE LANZAMIENTO")
        # Agrupamos por la columna 'start' para ver la evolución de lanzamientos
        series_por_año = df_filtrado.groupby('startYear').size().reset_index(name='Cantidad')
        fig3 = px.line(series_por_año, x='startYear', y='Cantidad', color_discrete_sequence=['#FF4B4B'])
        fig3.update_layout(xaxis_title="Año de Inicio")
        st.plotly_chart(fig3, use_container_width=True)
        
    st.divider()

    # FILA 3: TOP 10, TORTA Y DISPERSIÓN (3 Columnas)
    col_b1, col_b2, col_b3 = st.columns(3)
    
    with col_b1:
        st.subheader("TOP 10 SERIES")
        top_10 = df_filtrado.sort_values(by=['averageRating', 'numVotes'], ascending=False).head(10)
        
        for i, row in enumerate(top_10.itertuples(), 1):
            st.write(f"**{i}.** {row.primaryTitle} ({int(row.startYear) if pd.notnull(row.startYear) else ''}) — {row.averageRating} ⭐")
            
    with col_b2:
        st.subheader("GENERO MAS POPULARES POR VOTOS")
        votos_por_genero = df_filtrado.groupby('genres')['numVotes'].sum().reset_index()
        fig4 = px.pie(votos_por_genero, values='numVotes', names='genres', hole=0.2)
        st.plotly_chart(fig4, use_container_width=True)
        
    with col_b3:
        st.subheader("PUNTUACIÓN VS VOTOS")
        fig5 = px.scatter(df_filtrado, x="numVotes", y="averageRating", 
                          opacity=0.4, color_discrete_sequence=['#1f77b4'],
                          hover_data=['primaryTitle', 'startYear'])
        st.plotly_chart(fig5, use_container_width=True)

else:
    st.error("❌ No hay registros que coincidan con los filtros seleccionados.")
