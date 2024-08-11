import streamlit as st

# Página de administración
if st.button("Ir a la página de administración"):
    st.title("Página de administración")
    with st.form("admin_form"):
        username = st.text_input("Usuario:")
        password = st.text_input("Contraseña:", type="password")
        submit_button = st.form_submit_button("Agregar usuario")

        if submit_button:
            # Agregar usuario a la base de datos
            # (en este caso, solo se muestra un mensaje de confirmación)
            st.write("Usuario agregado con éxito")

# Página de login
if st.button("Ir a la página de login"):
    st.title("Página de login")
    with st.form("login_form"):
        username = st.text_input("Usuario:")
        password = st.text_input("Contraseña:", type="password")
        submit_button = st.form_submit_button("Iniciar sesión")

        if submit_button:
            # Verificar la autenticación
            if username == "admin" and password == "password":  # Reemplaza con tus credenciales
                # Si la autenticación es correcta, muestra el contenido protegido
                st.write("Bienvenido!")
                # Aquí puedes agregar el código para generar actividades
            else:
                # Si la autenticación es incorrecta, muestra un mensaje de error
                st.error("Contraseña o usuario incorrecto")

# Código para generar actividades
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
        "stop": ["\n"]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error al generar actividades: {response.status_code}"

# Generar y mostrar actividades cuando se presiona el botón
if st.button("Generar actividades"):
    with st.form("actividades_form"):
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

# Información adicional
st.sidebar.header("Acerca de")
st.sidebar.info(
    "Esta aplicación genera actividades educativas personalizadas "
    "para ayudar a reforzar conceptos específicos en diferentes asignaturas y grados."
)
