import streamlit as st
import json
import hashlib
import os
import logging
import secrets

# Configuración de la página
st.set_page_config(page_title="Generador de Actividades", page_icon="📚")

# Constantes
USERS_FILE = 'users.json'
ADMIN_USER = "admin"  # Nombre de usuario del administrador
ADMIN_PASSWORD = "admin123"  # Contraseña predeterminada del administrador

# Configuración de logging
logging.basicConfig(level=logging.INFO)

# Cargar usuarios desde el archivo JSON
def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as file:
                return json.load(file)
        return {}
    except Exception as e:
        logging.error(f"Error al cargar usuarios: {e}")
        return {}

# Guardar usuarios en el archivo JSON
def save_users(users):
    try:
        with open(USERS_FILE, 'w') as file:
            json.dump(users, file)
    except Exception as e:
        logging.error(f"Error al guardar usuarios: {e}")

# Función para hashear contraseñas
def hash_password(password):
    salt = secrets.token_hex(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return salt + hashed_password.hex()

# Inicializar el administrador si no existe
def initialize_admin():
    users = load_users()
    if ADMIN_USER not in users:
        hashed_password = hash_password(ADMIN_PASSWORD)
        users[ADMIN_USER] = hashed_password
        save_users(users)

# Llamar a la función de inicialización al inicio
initialize_admin()

# Función para verificar las credenciales
def check_credentials(username, password):
    if not username or not password:
        return False
    users = load_users()
    if username in users:
        hashed_password = users[username]
        salt = hashed_password[:32]
        hashed_password = hashed_password[32:]
        new_hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        if hashed_password == new_hashed_password.hex():
            print("Contraseña correcta")
        else:
            print("Contraseña incorrecta")
        return hashed_password == new_hashed_password.hex()
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
if 'username' not in st.session_state:
    st.session_state.username = None

# Función para generar actividades
def generar_actividades(concepto, asignatura, grado):
    # Implementa la lógica de generación de actividades aquí
    return f"Actividades para {concepto} en {asignatura} para el grado {grado}"

# Página de login
def login_page():
    st.title("Login")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar sesión"):
        if check_credentials(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            
            if username == ADMIN_USER:
                st.session_state.page = 'register'
            else:
                st.session_state.page = 'main'
                
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

# Página de registro (Solo accesible para el administrador)
def register_page():
    st.title("Registro de Usuario")
    new_username = st.text_input("Nuevo Usuario")
    new_password = st.text_input("Nueva Contraseña", type="password")
    confirm_password = st.text_input("Confirmar Contraseña", type="password")
    
    if st.button("Crear Cuenta"):
        if new_password != confirm_password:
            st.error("Las contraseñas no coinciden")
        elif add_user(new_username, new_password):
            st.success("Cuenta creada con éxito.")
            st.session_state.page = 'main'
            st.experimental_rerun()
        else:
            st.error("El nombre de usuario ya existe")
    
    if st.button("Volver"):
        st.session_state.page = 'main'
        st.experimental_rerun()

# Página principal
def main_page():
    st.title("Generador de Actividades de Aprendizaje")

    # Botón de logout
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.page = 'login'
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

# Información adicional (visible en todas las páginas)
st.sidebar.header("Acerca de")
st.sidebar.info(
    "Esta aplicación genera actividades educativas personalizadas "
    "para ayudar a reforzar conceptos específicos en diferentes asignaturas y grados."
)

# Control de flujo principal
if st.session_state.authenticated:
    if st.session_state.page == 'register':
        register_page()
    else:
        main_page()
else:
    login_page()
