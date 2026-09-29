import streamlit as st
import pandas as pd

st.set_page_config(page_title="Examen en Línea (5 Opciones)", layout="centered")
st.title("📝 Examen en Línea")

# 1. Cargar preguntas desde el Excel
@st.cache_data
def cargar_preguntas():
    return pd.read_excel("preguntas.xlsx")

df = cargar_preguntas()

respuestas_usuario = {}

# 2. Formulario del Examen
with st.form("examen_5_opciones_form"):
    for index, row in df.iterrows():
        st.write(f"### {index + 1}. {row['Pregunta']}")
        
        # Mapeo de opciones e imágenes
        opciones_texto = [
            row['OpcionA'], row['OpcionB'], row['OpcionC'], row['OpcionD'], row['OpcionE']
        ]
        
        imagenes_opciones = [
            row.get('ImagenA'), row.get('ImagenB'), row.get('ImagenC'), row.get('ImagenD'), row.get('ImagenE')
        ]
        
        # Verificar si hay al menos una imagen en las opciones
        tiene_imagenes = any(pd.notna(img) for img in imagenes_opciones)
        
        # Si hay imágenes, creamos 5 columnas para mostrarlas ordenadamente
        if tiene_imagenes:
            cols = st.columns(5)
            etiquetas = ['A', 'B', 'C', 'D', 'E']
            
            for i, col in enumerate(cols):
                with col:
                    st.caption(f"**{etiquetas[i]}) {opciones_texto[i]}**")
                    if pd.notna(imagenes_opciones[i]):
                        st.image(imagenes_opciones[i], use_container_width=True)
        
        # Radio button para la selección de respuestas (A, B, C, D, E)
        # Se filtran opciones vacías por si alguna pregunta solo tiene 3 o 4 opciones
        opciones_validas = [opt for opt in opciones_texto if pd.notna(opt)]
        
        respuestas_usuario[index] = st.radio(
            "Selecciona tu respuesta:",
            opciones_validas,
            key=f"q_{index}",
            index=None
        )
        st.divider()
        
    enviado = st.form_submit_button("Enviar Respuestas")

# 3. Resultado
if enviado:
    puntaje = 0
    total = len(df)
    
    for index, row in df.iterrows():
        if respuestas_usuario[index] == row['Correcta']:
            puntaje += 1
            
    porcentaje = (puntaje / total) * 100
    st.header(f"Resultado: {puntaje} / {total} ({porcentaje:.1f}%)")
    
    if porcentaje >= 60:
        st.success("¡Felicidades, has aprobado!")
    else:
        st.error("No has alcanzado el puntaje mínimo.")