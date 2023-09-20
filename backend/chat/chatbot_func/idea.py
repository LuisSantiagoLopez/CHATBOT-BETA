from .langchain_gpt import chatgpt_langchain

def create_idea_py(session):
  prompt = f"""Tu tarea es crear una idea relevante e impactante para el Instagram del negocio. Primero, elige un tema interesante relacionado con su negocio que también pueda ser de interés para su público objetivo. Luego, selecciona un formato para representar tu tema, como contar un hecho interesante, recomendar herramientas para su audiencia (que no compitan con el negocio), una actividad interactiva para su audiencia, contar una historia, escribir un artículo de noticias o cualquier otro formato creativo. Finalmente, con tu tema y formato, crea la idea para la publicación. Al crear tu idea, por favor considera cualquier retroalimentación previa del negocio. Tu resultado únicamente debe ser un diccionario JSON con las claves 'tema', 'formato' e 'idea'."""

  response = chatgpt_langchain(prompt, session, 'gpt-4')

  return response

def change_idea_py(session, data):
  prompt = f"""Tu tarea es recibir la retroalimentación dentro de triple comillas invertidas del negocio a tu idea anterior y crear una nueva idea para Instagram. Primero, analiza la retroalimentación del negocio a tu idea dentro de triple comillas invertidas. Basándote en tu análisis de la retroalimentación del usuario, crea una nueva idea. Primero, elige un tema interesante relacionado con su negocio que también pueda ser de interés para su público objetivo. Luego, selecciona un formato para representar tu tema, como contar un hecho interesante, recomendar herramientas para su audiencia (que no compitan con el negocio), una actividad interactiva para su audiencia, contar una historia, escribir un artículo de noticias o cualquier otro formato creativo. Finalmente, con tu tema y formato, crea la nueva idea para la publicación. Tu resultado únicamente debe ser un diccionario JSON con las claves 'tema', 'formato' e 'idea'.
  Retroalimentación: '{data.get('feedback')}'"""

  response = chatgpt_langchain(prompt, session, 'gpt-4')

  return response

