import os
import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv
from google.generativeai.types import HarmCategory, HarmBlockThreshold

MAX_RETRIES = 5  # Maximum number of attempts for the Gemini API

summary_instructions = """Para generar el resumen de un juicio debes redactar un resumen para ver los miembros del jurado que más interactuaron y los eventos más significativos en el juicio, así como la deliberacion en la fase de belief confrontation, es decir, aquellos que contribuyeron más al veredicto final. Es muy importante escribir un resumen de la interaccion de los jurados en la deliberacion a modo de historia que el lector pueda entender. Que un jurado tenga una creencia acerca de un hecho alta, es decir, que cree que el hecho es verídico, quiere decir que cree que el acusado es culpable. El abogado del acusado quiere que se le encuentre inocente, por lo que sus esfuerzos siempre van orientados a persuadir al jurado a emitir un voto de no culpable. Si la opinion acerca de un hecho es menor que -15 es porque cree que es falso, si es mayor que 15 se cree que es verdadero. En otro caso el jurrado no está seguro de lo acontecido."""


class Trial_summary_generator:
    def __init__(self, config_file='.env'):
        # Cargar las variables de entorno desde el archivo .env
        load_dotenv(config_file)

        # Configurar la API de Gemini AI utilizando la clave de API
        self.api_key = os.environ['GENAI_API_KEY']
        genai.configure(api_key=self.api_key)
        self.start_new_chat(summary_instructions)
        
    def start_new_chat(self, system_instruction):
        self.chat = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
            system_instruction = system_instruction
        ).start_chat(history=[])

    def generate_summary(self, trial_log):
        message = "Genera un resumen de lo acontecido en el juicio a partir de la siguiente secuencia de eventos: "
        message += trial_log
        return self.send_message(message)
        
        # self.start_new_chat(summary_instructions)

    def send_message(self, text, retry_count=0):
        # Get the characters from Gemini AI
        try:
            response = self.chat.send_message(text)
            return response.text.strip() if response else None
        except genai.types.BlockedPromptException as e:
            # Handle exception if the request is blocked
            print(f"The prompt was blocked: {e}")
            return None
        except ResourceExhausted as e:
            # Retry if resource limit is reached
            if retry_count < MAX_RETRIES:
                time.sleep(2 ** retry_count)  # Implement exponential backoff
                return self.send_message(text, retry_count + 1)
            else:
                raise e

# if __name__ == "__main__":

#     print("Ok")

