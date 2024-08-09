import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(page_title="Generador de Actividades", page_icon="📚")

# Título de la aplicación
st.title("Generador de Actividades de Aprendizaje")

# Formulario para ingresar los datos
with st.form("input_form"):
    concepto = st.text_input("Concepto a reforzar:")
    asignatura = st.text_input("Asignatura:")
    grado = st.text_input("Grado:")
    submit_button = st.form_submit_button("Generar Actividades")

# Función para generar actividades
def generar_actividades(concepto, asignatura, grado):
    api_key = st.secrets["API_KEY"]
    url = "https://api.together.xyz/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": "Eres un asistente especializado en educación que genera actividades para reforzar conceptos."},
            {"role": "user", "content": f"Genera 3 actividades para reforzar el concepto de '{concepto}' en la asignatura de {asignatura} para estudiantes de {grado} grado. Las actividades deben ser variadas, interactivas y adecuadas para el nivel educativo."}
        ],
        "max_tokens": 2512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["<|eot_id|>"]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error al generar actividades: {response.status_code}"

# Generar y mostrar actividades cuando se presiona el botón
if submit_button:
    if concepto and asignatura and grado:
        with st.spinner("Generando actividades..."):
            actividades = generar_actividades(concepto, asignatura, grado)
            st.subheader("Actividades Generadas:")
            st.write(actividades)
    else:
        st.warning("Por favor, completa todos los campos antes de generar actividades.")

# Información adicional
st.sidebar.header("Acerca de")
st.sidebar.info(
    "Esta aplicación genera actividades educativas personalizadas "
    "para ayudar a reforzar conceptos específicos en diferentes asignaturas y grados."
)
