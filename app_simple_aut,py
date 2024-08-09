import streamlit as st
import requests
import json
import hashlib

# Configuración de la página
st.set_page_config(page_title="Generador de Actividades", page_icon="📚")

# Cargar usuarios desde el archivo JSON
def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)

# Función para hashear contraseñas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Función para verificar las credenciales
def check_credentials(username, password):
    users = load_users()
    if username in users:
        return users[username] == hash_password(password)
    return False

# Inicializar el estado de la sesión
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

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

# Interfaz de login
if not st.session_state.authenticated:
    st.title("Login")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        if check_credentials(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")
else:
    # Interfaz principal de la aplicación
    st.title("Generador de Actividades de Aprendizaje")

    # Botón de logout
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.experimental_rerun()

    st.sidebar.write(f"Bienvenido, {st.session_state.username}!")

    # Formulario para ingresar los datos
    with st.form("input_form"):
        concepto = st.text_input("Concepto a reforzar:")
        asignatura = st.text_input("Asignatura:")
        grado = st.text_input("Grado:")
        submit_button = st.form_submit_button("Generar Actividades")

    # Generar y mostrar actividades cuando se presiona el botón
    if submit_button:
        if concepto and asignatura and grado:
            with st.spinner("Generando actividades..."):
                actividades = generar_actividades(concepto, asignatura, grado)
                st.subheader("Actividades Generadas:")
                st.write(actividades)
        else:
            st.warning("Por favor, completa todos los campos antes de generar actividades.")

# Información adicional (visible incluso sin autenticación)
st.sidebar.header("Acerca de")
st.sidebar.info(
    "Esta aplicación genera actividades educativas personalizadas "
    "para ayudar a reforzar conceptos específicos en diferentes asignaturas y grados."
)
