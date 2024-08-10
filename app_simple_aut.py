import streamlit as st
import requests
import json
import hashlib
import os

# Configuración de la página
st.set_page_config(page_title="Generador de Actividades", page_icon="📚")

# Constantes
USERS_FILE = 'users.json'

# Cargar usuarios desde el archivo JSON
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Guardar usuarios en el archivo JSON
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file)

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
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Función para generar actividades (debes implementar esta función)
def generar_actividades(concepto, asignatura, grado):
    pass  # Elimina este 'pass' y añade el código correspondiente

# Página de login
def login_page():
    st.title("Login")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        if check_credentials(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.page = 'main'
        else:
            st.error("Usuario o contraseña incorrectos.")

# Página principal
def main_page():
    st.title("Generador de Actividades de Aprendizaje")

    # Botón de logout
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.page = 'login'

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

# Información adicional (visible en todas las páginas)
st.sidebar.header("Acerca de")
st.sidebar.info(
    "Esta aplicación genera actividades educativas personalizadas "
    "para ayudar a reforzar conceptos específicos en diferentes asignaturas y grados."
)

# Control de flujo principal
if st.session_state.authenticated:
    main_page()
else:
    login_page()
