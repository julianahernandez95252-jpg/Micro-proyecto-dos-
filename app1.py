import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly 
import plotly.express as px 

#Texto
st.title("Este es el titulo de mi app")
st.header("Este es el encabezado")
st.subheader("Este es un subencabezado")
st.text("Esto es texto simple")
st.markdown("Esto es un texto en *cursiva* y esto en **negrilla**")

st.code("import pandas as pd", language = 'python')
st.latex(r"E = mc^2")

#Input
nombre = st.text_input("Cual es tu nombre")
st.write(f"Hola,{nombre}!")

fecha = st.date_input("Escoja una fecha")
st.write(f"La fecha seleccionada es: {fecha}")

#Crear botones 
if st.button("Salir"):
    st.write(f"Hata la proxima,{nombre}!")

#Crear un slider
edad = st.slider("Cuantos años tienes", min_value=0, max_value=100, value=30)
st.write(f"Tienes {edad} años")

#Menu desplegable 
opcion = st.selectbox("Elige tu equipo:", ["1. Real Madrid","2. Barca","3. Bayern","4. Inter"])
st.write(f"Elegiste: {opcion}")

#Pandas
data = {"Nombre": ["Juan","Pedro","Ana"],
        "Edad":[15,20,30]}
df = pd.DataFrame(data)
st.write(df)

#Subir archivos 
Upload_file = st.file_uploader("Escoja un archivo",type = "csv")
if Upload_file is not None:
    df = pd.read_csv(Upload_file)
    st.write(df)

#Graficas
#Grafica de linea
data = pd.DataFrame(np.random.randn(10,2), columns=["A","B"])
st.line_chart(data)

st.bar_chart(data)