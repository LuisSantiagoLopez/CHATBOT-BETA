from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
from .models import ChatSession, BusinessDetails, ChatLog

def chatgpt_langchain(session, prompt, model):

    # Guardamos el mensaje del usuario como el prompt. 
    ChatLog.objects.create(
    chat_session = session,
    message_type = 'USER',
    message_content = prompt,
    )

    # Seleccionamos el modelo y tipo de memoria que usaremos.
    chat = ChatOpenAI(temperature=0.5, model=model)
    memory = ConversationBufferMemory(return_messages=True)
    session_business_details = BusinessDetails.objects.get(chat_session=session)

    # Si existe un chatlog con esta sesión lo seleccionamos para meterlo en la memoria 
    if ChatLog.objects.filter(chat_session=session).exists():
        human_conversation_history = ChatLog.objects.filter(chat_session=session, message_type='USER')
        ai_conversation_history = ChatLog.objects.filter(chat_session=session, message_type='AI')
    else:
        human_conversation_history = []
        ai_conversation_history = []

    # Metemos cada input y output a la memoria 
    conversations = []
    for human_msg, ai_msg in zip(human_conversation_history, ai_conversation_history):
        input = human_msg.message_content
        output = ai_msg.message_content
        conversations.append({"input": input, "output": output})
        memory.save_context({"input": input}, {"output": output})

    # Este es el mensaje base del chat
    system_message_template = f"""Eres un útil administrador de comunidad de Instagram para {session_business_details.business_name}. Tu tarea es ayudarles a crear una publicación para su feed de Instagram. Se te pedirá que hagas una de las siguientes cosas: crear una idea, modificar una idea, crear una imagen, modificar una imagen, crear un pie de foto o modificar un pie de foto. Al hacerlo, debes tener en cuenta los detalles del negocio:
    Descripción del negocio: "{session_business_details.business_description}",
    Público objetivo: "{session_business_details.target_audience}""""

    # Montamos el mensaje con el chat prompt (system message), el prompt proviniente de la función, y el placeholder que es para guardar memoria 
    chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_message_template),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

    # Definimos la conversacion del primer chain con memoria 
    conversation = ConversationChain(
    llm=chat,
    prompt=chat_prompt,
    memory=memory,
    verbose=True
    )

    #Esta segunda chain es en la que manejamos los requests que no requieren de memoria 
    system_template = system_message_template
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt_2 = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    
    # Definimos el chain secundario 
    secondary_chain = LLMChain(
    llm=chat,
    prompt=chat_prompt_2,
    )

    # Recimimos una respuesta de o la chain sin memoria (ocupa menos tokens) o la chain con memoria
    with get_openai_callback() as cb:
        if prompt[0] == "1":
            response = secondary_chain.run(text=prompt)
            return response 
        else:
            response = conversation.predict(input=prompt)
            # Salvamos el mensaje de respuesta como un log en la base de datos 
            ChatLog.objects.create(
            chat_session = session,
            message_type = 'AI',
            message_content = response,
            )
            return response 