import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(page_title="Generador de Actividades", page_icon="📚")

# Título de la aplicación
st.title("Generador de Actividades de Aprendizaje")

# Función para llamar a la API
def llamar_api(prompt):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['API_KEY']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["<|eot_id|>"]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

# Formulario para ingresar los datos
with st.form("datos_actividad"):
    concepto = st.text_input("Concepto a reforzar")
    asignatura = st.text_input("Asignatura")
    grado = st.text_input("Grado o nivel educativo")
    
    submitted = st.form_submit_button("Generar Actividad")

# Generación de la actividad
if submitted:
    if concepto and asignatura and grado:
        with st.spinner("Generando actividad..."):
            prompt = f"""
            Genera una actividad educativa para reforzar el siguiente concepto:
            
            Concepto: {concepto}
            Asignatura: {asignatura}
            Grado o nivel: {grado}
            
            La actividad debe ser interactiva, adecuada para el nivel educativo especificado, y diseñada para asegurar la correcta fijación del concepto. 
            Incluye una breve descripción de la actividad, los objetivos de aprendizaje, los materiales necesarios (si los hay), y los pasos detallados para realizarla.
            """
            
            resultado = llamar_api(prompt)
            st.subheader("Actividad Generada")
            st.write(resultado)
    else:
        st.warning("Por favor, completa todos los campos antes de generar la actividad.")

# Instrucciones de uso
st.sidebar.header("Instrucciones")
st.sidebar.write("""
1. Ingresa el concepto que deseas reforzar.
2. Especifica la asignatura a la que pertenece el concepto.
3. Indica el grado o nivel educativo de los estudiantes.
4. Haz clic en "Generar Actividad" para obtener una actividad personalizada.
""")

# Nota sobre la API
st.sidebar.info("Esta aplicación utiliza la API de Together.xyz para generar actividades educativas personalizadas.")
