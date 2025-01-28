#librerias
import streamlit as st
from gtts import gTTS
import io
import tempfile
#importacion del modelo entrenado del chatbot
from brain import predict_class, get_response, intents
# Configuración de la página y logo en el titulo del chatbot
st.set_page_config(
    page_title="Chatbot docente",
    page_icon="https://cdn.icon-icons.com/icons2/3399/PNG/512/bot_icon_214984.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

#side bar 
#st.sidebar.markdown("<h1 style='font-size: 20px;text-align:center;'>Genera tu planeacion didactica con ayuda de un chatbot</h1>", unsafe_allow_html=True)
# imagen
#user_avatar = "https://cdn.icon-icons.com/icons2/3399/PNG/512/bot_icon_214984.png"
#st.sidebar.image(user_avatar, use_column_width=True)
# Header
image_url = 'https://img.freepik.com/foto-gratis/acuarela-color-rojo-oscuro-textura-fondo-pintado-mano-fondo-color-vino-tinto-acuarela_145343-192.jpg?size=626&ext=jpg'
st.markdown("""
    <style>
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 10px;
        background-color: #ffff;
    }
    
    .header-logo {
        width: 120px;
        height: 80px;
        margin: 0 10px;
    }
    
    .header-title {
        color: black;
        font-size: 1.5em;
        margin:0;
        text-align:center;
    }
    
    .subtopics {
        text-align: center;
        font-size: 1.5em;
        margin: 0;
        color:black;
    }
    
    .subtopics p {
        margin:0;
    }

    @media (max-width: 600px) {
        .header-title {
            font-size: 0.9em;
        }
        .subtopics {
            font-size: 1em;
        }
        .header-logo {
            width:60px;
            height: 60px;
        }
        
    }
    .circle-img {
        border-radius: 50%;
        width: 100px;
        height: 100px;
        object-fit: cover;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    
    </style>
    <div class="header-container">
        <div style="display: flex; justify-content: space-between; width: 100%; align-items: center;">
            <img src="https://th.bing.com/th/id/OIP.MQI9waMb4IGJ52U8KF5gmgHaHa?rs=1&pid=ImgDetMain" class="header-logo">
            <h3 class="header-title">Instituto Politecnico Nacional</h3>
            <img src="https://th.bing.com/th/id/R.8119ac7aaccd85c2837ae19087717f56?rik=3mREtV8uaKpCGg&pid=ImgRaw&r=0" class="header-logo">
        </div>
        <div class="subtopics">
            <p>Secretaría Académica</p>
            <p>Dirección de Educación Superior</p>
            <p>Unidad Profesional Interdisciplinaria Campus de Ingenieria Hidalgo</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Fondo de la app
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('{image_url}');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    """, unsafe_allow_html=True)
#menu de opciones 
Menu_paths ={
    #"Temario:Sistemas automotrices semestre 7-tecnologia de materiales automotrices": "Bot/automotricesSemestre7.docx",
    "Programa sinetico:Sistemas automotrices semestre 7-programasintetico-tecnologia de materiales automotrices": "Bot/SA_PS7.pdf",
    "Programa SineticoIngenieria mecatronica semestre 1-programasintetico-estructura y propiedades de los materiales": "Bot/M_PS1.pdf"
    #"Ingenieria mecatronica semestre 1-estructura y propiedades de los materiales": "Bot/ingenieriaMecatronica_1.docx"
   
}
#funcion  para hablar 
def speak(text):
    tts = gTTS(text=text, lang='es')
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    st.audio(audio_file, format='audio/mp3')
# Lógica del chatbot
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True
if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = "https://cdn.icon-icons.com/icons2/3399/PNG/512/bot_icon_214984.png"  # URL de la imagen del usuario

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.first_message:
    initial_message = "Hola, ¿en qué puedo ayudarte?."
    with st.chat_message("Bot"):
        st.markdown(initial_message)
    st.session_state.messages.append({"role": "Bot", "content": initial_message})
    st.session_state.first_message = False
    speak(initial_message)

if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    insts = predict_class(prompt)
    res = get_response(insts, intents)

    with st.chat_message("Bot"):
        st.markdown(res)
    st.session_state.messages.append({"role": "Bot", "content": res})
    speak(res)
#menu desplegable de elecciones

Choose_temarios = st.multiselect("Planeaciones disponibles:", list(Menu_paths.keys()))
if Choose_temarios:
    for programa in Choose_temarios:
        file_path=Menu_paths[programa]
           # Crea un botón para descargar el archivo
        with open(file_path, "rb") as file:
            btn = st.download_button(
                label=f"Descargar {programa}",
                data=file,
                file_name=file_path.split("/")[-1],  # Nombre del archivo al descargar
                mime="application/octet-stream"
            )