import streamlit as st
import json
import hashlib
import os

# Configuración de la página
st.set_page_config(page_title="Administrador de Usuarios", page_icon="🔑")

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

# Función para agregar un nuevo usuario
def add_user(username, password):
    users = load_users()
    if username not in users:
        users[username] = hash_password(password)
        save_users(users)
        return True
    return False

# Página de administración de usuarios
def admin_page():
    st.title("Administrador de Usuarios")

    new_username = st.text_input("Nuevo Usuario")
    new_password = st.text_input("Nueva Contraseña", type="password")
    confirm_password = st.text_input("Confirmar Contraseña", type="password")

    if st.button("Agregar Usuario"):
        if new_password != confirm_password:
            st.error("Las contraseñas no coinciden.")
        elif add_user(new_username, new_password):
            st.success(f"Usuario '{new_username}' agregado exitosamente.")
        else:
            st.error(f"El usuario '{new_username}' ya existe.")

# Mostrar la página de administración
admin_page()
