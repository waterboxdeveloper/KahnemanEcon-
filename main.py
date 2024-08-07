import streamlit as st
from streamlit_chat import message
from ai import AIAssistant
import os
from dotenv import load_dotenv

load_dotenv()

# Ruta al archivo PDF fijo
PDF_PATH = os.getenv("PDF_PATH")

# Crear una instancia de AIAssistant
assistant = AIAssistant(PDF_PATH)

def on_input_change():
    """
    Función que se llama cuando el usuario cambia el texto de entrada.
    Agrega la entrada del usuario al historial y obtiene la respuesta del asistente.
    Actualiza el historial de la conversación y el estado del chat.
    """
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    
    # Obtener la respuesta del asistente utilizando la entrada del usuario
    response, updated_history = assistant.generate_response(user_input, st.session_state.conversation_history)
    
    # Agregar la respuesta generada al historial de respuestas
    st.session_state.generated.append(response)
    # Actualizar el historial de conversación con la nueva respuesta
    st.session_state.conversation_history = updated_history

def on_btn_click():
    """
    Función que se llama al hacer clic en el botón de borrar mensajes.
    Limpia el historial de conversación y las respuestas generadas.
    """
    del st.session_state.past[:]
    del st.session_state.generated[:]
    st.session_state.conversation_history = ""

def main():
    """
    Función principal que configura y ejecuta la aplicación Streamlit.
    Muestra el título, el texto del PDF, el historial de la conversación y
    proporciona un campo de entrada para las preguntas del usuario.
    """
    st.title("Nombre chingón para el bot")  

    # Extraer el texto del PDF fijo usando la instancia de AIAssistant
    pdf_text = assistant.pdf_text
    # Mostrar el texto del PDF en un área de texto deshabilitada
    st.text_area("Responderá tus preguntas sobre este documento ⬇️", pdf_text, height=300, disabled=True)

    # Inicializar el estado de la conversación si no está establecido
    st.session_state.setdefault('past', [])
    st.session_state.setdefault('generated', [])
    st.session_state.setdefault('conversation_history', "")

    # Mostrar el historial de conversación
    chat_placeholder = st.empty()
    with chat_placeholder.container():
        # Mostrar mensajes anteriores en el historial de conversación
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
            message(st.session_state['generated'][i], key=f"{i}", allow_html=True)

        # Botón para borrar el historial de mensajes
        st.button("Borrar mensajes", on_click=on_btn_click)

    # Entrada de texto del usuario para hacer preguntas
    with st.container():
        st.text_input("Haz una pregunta sobre el reglamento 📕:", on_change=on_input_change, key="user_input")

if __name__ == "__main__":
    main()
