import streamlit as st
import json
import hashlib
import os

# Configuración de la página
st.set_page_config(page_title="Administración de Usuarios", page_icon="🔐")

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

# Función para eliminar un usuario
def delete_user(username):
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
        return True
    return False

# Función para la página de administración
def admin_page():
    st.title("Administración de Usuarios")
    
    # Sección para agregar usuarios
    st.header("Agregar Nuevo Usuario")
    new_username = st.text_input("Nuevo Usuario")
    new_password = st.text_input("Nueva Contraseña", type="password")
    confirm_password = st.text_input("Confirmar Contraseña", type="password")
    if st.button("Agregar Usuario"):
        if new_password != confirm_password:
            st.error("Las contraseñas no coinciden.")
        elif add_user(new_username, new_password):
            st.success(f"Usuario {new_username} agregado exitosamente.")
            st.rerun()  # Recargar la página para mostrar el nuevo usuario
        else:
            st.error("El usuario ya existe.")
    
    # Sección para listar y eliminar usuarios
    st.header("Usuarios Existentes")
    users = load_users()
    if not users:
        st.write("No hay usuarios registrados.")
    else:
        for username in users.keys():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(username)
            with col2:
                if st.button("Eliminar", key=f"delete_{username}"):
                    if delete_user(username):
                        st.success(f"Usuario {username} eliminado exitosamente.")
                        st.rerun()  # Recargar la página para actualizar la lista de usuarios
                    else:
                        st.error(f"Error al eliminar el usuario {username}.")
    
    # Botón para cerrar sesión
    if st.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.session_state.page = 'login'
        st.rerun()

# Ejecución de la página de administración
if __name__ == "__main__":
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        admin_page()
    else:
        st.error("No tienes permiso para acceder a esta página. Por favor, inicia sesión como administrador.")
