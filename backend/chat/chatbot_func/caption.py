from .langchain_gpt import chatgpt_langchain
from ..models import BusinessDetails, Idea, Image
import json

def create_caption_py(session):
 
 chosen_idea = Idea.objects.filter(chosen=True, chat_session=session).first()
 chosen_idea_idea_field_pydict = json.loads(chosen_idea.text)
 chosen_idea_idea_field_str = chosen_idea_idea_field_pydict[idea]

 chosen_image = Image.objects.filter(chosen=True, chat_session=session).first()
 chosen_image_image_field_pydict = json.loads(chosen_image.text)
 chosen_image_image_field_str = chosen_image_image_field_pydict[design_prompt]

 session_business_description = BusinessDescription.objects.get(chat_session=session)
 
 prompt = f"""Tu tarea es generar un pie de foto para instagram a partir de una idea y una descripción de una ilustración, ambos mostrados a continuación. Tu pie de foto debe ser relevante a la idea e ilustraciñin e incluir alguna referencia al negocio. Debe invitar a los seguidores a seguir la cuenta al final. Debe estar escrita con el estilo del negocio, indicado a continuación. Tu resultado únicamente debe ser el texto para el pie de foto.
 Idea: '{chosen_idea_idea_field_str}',
 Descripción de la ilustración: '{chosen_image_image_field_str}',
 Estilo del negocio: '{session_business_description.writing_style}'"""

 response = chatgpt_langchain(prompt, session, "gpt-4")

 return response 

def change_caption_py(session, data):
 chosen_idea = Idea.objects.filter(chosen=True, chat_session=session).first()
 chosen_idea_idea_field_pydict = json.loads(chosen_idea.text)
 chosen_idea_idea_field_str = chosen_idea_idea_field_pydict[idea]

 chosen_image = Idea.objects.filter(chosen=True, chat_session=session).first()
 chosen_image_image_field_pydict = json.loads(chosen_image.text)
 chosen_image_image_field_str = chosen_image_image_field_pydict[design_prompt]

 session_business_description = BusinessDescription.objects.get(chat_session=session)
 
 prompt = f"""Tu tarea es recibir la retroalimentación dentro de triple comillas invertidas del negocio a tu pie de foto anterior y crear una nueva idea para Instagram. Tu nueva pie de foto debe ser relevante a la idea e ilustraciñin e incluir alguna referencia al negocio. Debe invitar a los seguidores a seguir la cuenta al final. Debe estar escrita con el estilo del negocio, indicado a continuación. Tu resultado únicamente debe ser el texto para la nueva pie de foto.
 Retroalimentación: '{data.get('feedback')}',
 Idea: '{chosen_idea_idea_field_str}',
 Descripción de la ilustración: '{chosen_image_image_field_str}',
 Estilo del negocio: '{session_business_description.writing_style}'"""

 response = chatgpt_langchain(prompt, session, "gpt-4")

 return response 

# sep 19: necesitas terminar los captions y después el resto del backend. Habla con Ethan para ver cómo funciona su parte y genera el frontend para los dos. 