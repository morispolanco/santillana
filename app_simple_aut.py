import streamlit as st
import json
import hashlib
import os

# Configuración de la página
st.set_page_config(page_title="Generador de Actividades", page_icon="📚")

# Constantes
USERS_FILE = 'users.json'
ADMIN_USER = "admin"  # Nombre de usuario del administrador

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

# Inicializar el administrador si no existe
def initialize_admin():
    users = load_users()
    if ADMIN_USER not in users:
        users[ADMIN_USER] = hash_password("admin123")  # Establece la contraseña predeterminada
        save_users(users)

# Llamar a la función de inicialización al inicio
initialize_admin()

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
    col1, col2 = st.columns(2)
    if st.button("Iniciar sesión"):
        if check_credentials(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.page = 'main'
            st.experimental_rerun()

    if st.session_state.username == ADMIN_USER:
        if st.button("Registrarse"):
            st.session_state.page = 'register'
            st.experimental_rerun()

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
