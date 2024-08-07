import os
import google.generativeai as genai
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# Cargar variables de entorno desde el archivo .env
load_dotenv()
api_key = os.getenv("API_KEY")  # Obtener la clave API de las variables de entorno
genai.configure(api_key=api_key)  # Configurar la API de Google Generative AI con la clave

# Configuración del modelo de generación
generation_config = {
    "temperature": 1,  # Controla la creatividad de la respuesta (valor alto = respuestas más creativas)
    "top_p": 0.95,     # Controla la probabilidad acumulativa para la generación de texto
    "top_k": 64,       # Número de opciones principales a considerar durante la generación de texto
    "max_output_tokens": 8192,  # Número máximo de tokens en la respuesta generada
    "response_mime_type": "text/plain",  # Tipo MIME para la respuesta
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  # Nombre del modelo de generación
    generation_config=generation_config,  # Configuración del modelo
)

class AIAssistant:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path  # Ruta al archivo PDF
        self.pdf_text = self._load_pdf_text()  # Cargar el texto del PDF
        self.chat_session = self._initialize_chat()  # Inicializar la sesión de chat

    def _load_pdf_text(self):
        try:
            with open(self.pdf_path, "rb") as file:
                reader = PdfReader(file)  # Leer el archivo PDF
                text = ""
                for page in reader.pages:
                    text += page.extract_text()  # Extraer texto de cada página
            return text
        except Exception as e:
            raise Exception(f"Error al cargar el PDF: {e}")  # Manejar errores al cargar el PDF

    def _initialize_chat(self):
        # Configurar la sesión de chat con un historial inicial
        return model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        "Hola, ¿cómo puedo ayudarte con el reglamento?\n",  # Mensaje inicial del usuario
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "¡Hola! Estoy aquí para responder tus preguntas sobre el reglamento de la universidad.\n",  # Mensaje inicial del modelo
                    ],
                },
            ]
        )

    def generate_response(self, prompt, conversation_history):
        context = self.pdf_text  # El contexto es el texto completo del PDF

        # Verificar si es el primer mensaje de la conversación
        full_prompt = f"{context}\n{conversation_history}\nUsuario: {prompt}\nMarcos:"

        try:
            # Enviar el mensaje al modelo y obtener la respuesta
            response = self.chat_session.send_message(full_prompt)
            
            # Agregar la respuesta generada al historial de la conversación
            conversation_history += f"\nUsuario: {prompt}\nMarcos: {response.text}"

            return response.text, conversation_history
        except Exception as e:
            raise Exception(f"Error al generar la respuesta: {e}")  # Manejar errores al generar la respuesta

# Uso del AIAssistant
pdf_path = "/Users/egc/Documents/ECONOMÍA/tesis/Reglamento Facultad de Economía.pdf"  # Ruta al archivo PDF
assistant = AIAssistant(pdf_path)  # Crear una instancia del asistente con el PDF

# Ejemplo de interacción
user_input = "¿Cuál es el horario de atención de la facultad?"  # Pregunta del usuario
conversation_history = ""  # Inicializar el historial de la conversación
response, conversation_history = assistant.generate_response(user_input, conversation_history)  # Generar la respuesta
print(response)  # Imprimir la respuesta generada
