from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.callbacks import get_openai_callback
from token_usage import token_usage
from .models import ChatSession

def gpt4_langchain()
    # Lo primero que tengo que hacer es definir la sesión de chat a partir de los datos que el usuario proveyó en ChatSession


    system_message_template = f"You are a community manager for {}
    
    You are a helpful instagram content creator for this client's instagram: '{variables['program_description']}' with this target audience: '{variables['target_segment']}'. Help them execute a variety of tasks related with their instagram content marketing."

    chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_message_template),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])
