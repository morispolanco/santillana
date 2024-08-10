import streamlit as st
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

# Función para agregar un nuevo usuario
def add_user(username, password):
    users = load_users()
    if username not in users:
        users[username] = hash_password(password)
        save_users(users)
        return True
    return False

# Inicializar el estado de la sesión
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Función para la página de administración
def admin_page():
    st.title("Administración de Usuarios")

    new_username = st.text_input("Nuevo Usuario")
    new_password = st.text_input("Nueva Contraseña", type="password")
    confirm_password = st.text_input("Confirmar Contraseña", type="password")

    if st.button("Agregar Usuario"):
        if new_password != confirm_password:
            st.error("Las contraseñas no coinciden.")
        elif add_user(new_username, new_password):
            st.success(f"Usuario {new_username} agregado exitosamente.")
        else:
            st.error("El usuario ya existe.")

    if st.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.session_state.page = 'login'

# Página de login
def login_page():
    st.title("Login")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar sesión"):
        if check_credentials(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.page = 'admin' if username == 'admin' else 'main'
        else:
            st.error("Usuario o contraseña incorrectos.")

# Página principal
def main_page():
    st.title("Generador de Actividades de Aprendizaje")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.page = 'login'

    st.sidebar.write(f"Bienvenido, {st.session_state.username}!")

    with st.form("input_form"):
        concepto = st.text_input("Concepto a reforzar:")
        asignatura = st.text_input("Asignatura:")
        grado = st.text_input("Grado:")
        submit_button = st.form_submit_button("Generar Actividades")

    if submit_button:
        if concepto and asignatura and grado:
            with st.spinner("Generando actividades..."):
                actividades = generar_actividades(concepto, asignatura, grado)
                st.subheader("Actividades Generadas:")
                st.write(actividades)
        else:
            st.warning("Por favor, completa todos los campos antes de generar actividades.")

# Control de flujo principal
if st.session_state.authenticated:
    if st.session_state.page == 'admin':
        admin_page()
    else:
        main_page()
else:
    login_page()
