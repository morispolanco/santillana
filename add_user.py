import json
import hashlib
import os

USERS_FILE = 'users.json'

# Función para cargar usuarios
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Función para guardar usuarios
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
        print(f"Usuario {username} agregado exitosamente.")
    else:
        print(f"El usuario {username} ya existe.")

# Solicitar al administrador que ingrese el nombre de usuario y la contraseña
if __name__ == "__main__":
    username = input("Ingrese el nombre de usuario: ")
    password = input("Ingrese la contraseña: ")
    add_user(username, password)
