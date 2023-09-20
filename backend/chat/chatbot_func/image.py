from .langchain_gpt import chatgpt_langchain
from ..models import BusinessDetails, Idea
import json 
import openai

def generate_image_dalle(image_prompt):
    response = openai.Image.create(
      prompt=image_prompt,
      n=4,
      size="1024x1024"
    )
    image_urls = response["data"]

    return image_urls

def create_image_py(session):
    chosen_idea = Idea.objects.filter(chosen=True, chat_session=session).first()
    chosen_idea_idea_field_pydict = json.loads(chosen_idea.text)
    chosen_idea_idea_field_str = chosen_idea_idea_field_pydict[idea]

    session_business_details = BusinessDetails.objects.get(chat_session=session)

    prompt = f"""Tu tarea es crear una descripción de una ilustración representativa para la idea dentro de triple comillas invertidas. Incorpora el estilo del negocio señalado a continuación. La descripción debe ser corta y la ilustración representativa de la idea. 
    La descripción debe incluir el estilo de la ilustración. Evita descripciones que requieran figuras humanas y caras. Al crear tu descripción, por favor considera cualquier retroalimentación previa del negocio. Tu resultado únicamente debe ser un diccionario JSON con la clave 'design_prompt'.
    Estilo del negocio: '{session_business_details.image_style}',
    Idea: ```{chosen_idea_idea_field_str}```"""

    image_prompt_español = chatgpt_langchain(prompt, session, "gpt-4")
    image_prompt_español_pydict = json.loads(image_prompt_español)
    image_prompt_español_text = image_prompt_español_pydict[design_prompt]

    prompt = f"1. Your task is to translate the following text from spanish to english: {image_prompt_español_text}. Your response must only be a JSON dictionary with the key 'translation'."

    response = chatgpt_langchain(prompt, session, "gpt-3")
    response_pydict = json.loads(response)
    response_text = response_pydict[translation]

    generate_image_dalle(response_text)

    return image_urls, image_prompt_español
  
def change_image_py(data, session):
    chosen_idea = Idea.objects.filter(chosen=True, chat_session=session).first()
    chosen_idea_idea_field_pydict = json.loads(chosen_idea.text)
    chosen_idea_idea_field_str = chosen_idea_idea_field_pydict[idea]

    session_business_details = BusinessDetails.objects.get(chat_session=session)

    prompt = f"""Tu tarea es recibir la retroalimentación dentro de triple comillas invertidas del negocio a tu descripción de una ilustración anterior y crear una nueva descripción para la idea señalada a continuación. La descripción debe ser corta y la ilustración representativa de la idea. La descripción debe incluir el estilo de la ilustración. Evita descripciones que requieran figuras humanas y caras. Tu resultado debe ser únicamente un diccionario JSON con la clave 'design_prompt'.
    Retroalimentación: ```{data.get('feedback')}```,
    Estilo del negocio: '{session_business_details.image_style}',
    Idea: '{chosen_idea_idea_field_str}'"""

    image_prompt_español = chatgpt_langchain(prompt, session, "gpt-4")
    image_prompt_español_pydict = json.loads(image_prompt_español)
    image_prompt_español_text = image_prompt_español_pydict[design_prompt]

    prompt = f"1. Your task is to translate the following text from spanish to english: {image_prompt_español_text}. Your response must only be a JSON dictionary with the key 'translation'."

    response = chatgpt_langchain(prompt, session, "gpt-3")
    response_pydict = json.loads(response)
    response_text = response_pydict[translation]

    generate_image_dalle(response_text)

    return image_urls, image_prompt_español
