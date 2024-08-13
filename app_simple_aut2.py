import streamlit as st
import requests
import json
import hashlib

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'users' not in st.session_state:
    st.session_state.users = {'admin': hashlib.sha256('password'.encode()).hexdigest()}
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Login function
def login(username, password):
    if username in st.session_state.users and st.session_state.users[username] == hash_password(password):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        return True
    return False

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None

# Function to add new user (admin only)
def add_user(username, password):
    if username not in st.session_state.users:
        st.session_state.users[username] = hash_password(password)
        return True
    return False

# Configuración de la página
st.set_page_config(page_title="Generador de Actividades", page_icon="📚")

# Login/Logout UI
if not st.session_state.logged_in:
    st.title("Inicio de Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar Sesión"):
        if login(username, password):
            st.success("Inicio de sesión exitoso!")
        else:
            st.error("Usuario o contraseña incorrectos")
else:
    # Main application UI (only shown when logged in)
    st.title("Generador de Actividades de Aprendizaje")
    
    st.sidebar.button("Cerrar Sesión", on_click=logout)

    if st.session_state.current_user == 'admin':
        st.sidebar.title("Panel de Administrador")
        with st.sidebar.expander("Agregar Nuevo Usuario"):
            new_username = st.text_input("Nuevo Usuario")
            new_password = st.text_input("Nueva Contraseña", type="password")
            if st.button("Agregar Usuario"):
                if add_user(new_username, new_password):
                    st.success(f"Usuario {new_username} agregado exitosamente")
                else:
                    st.error("El usuario ya existe")

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
