
import json
import traceback
from openai import OpenAI
from controller.BaseController import BaseController
from globals import MODEL_OPENAI, OPENAI_API_KEY


class BotController(BaseController):
    
    def __init__(self):
        self.prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Eres un bot que se encarga de ayudar al usuario a conocer información sobre nuestro sistema de parkings, como disponibilidad de un parking,
obtener predicciones de un parking, saber que parkings estan disponible, etc.
Aquí está listado de parkings, el campo 'ocupation' indica cuatas plazas están ocupadas del total ('size'). El campo
'prediction' indica un listado de las predicciones de disponibilidad por cada hora del dia. El 'status' indica si el parking
está abierto o cerrado:
{context}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """
    
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
    def query(self, query, history, context):
        messages = [
            {
                "role": "system",
                "content": self.prompt.replace("{context}", json.dumps(context))
            },
            *history[:20],
            {
                "role": "user",
                "content": query
            }
        ]
        
        return self.client.chat.completions.create(messages=messages, model=MODEL_OPENAI, temperature=0.7).choices[0].message.content        
                
        