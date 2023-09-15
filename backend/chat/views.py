"""
La arquitectura es la siguiente:
1. Hay un state o estado en el que la conversación está
2. La view del API llamada "decision tree" hace routing para cada función dependiendo del botón que el usuario presionó en el frontend así como el estado actual en el que se encuentra. 
3. La función correspondiente procesa el request, cambia el estado si es necesario, y devuelve el response. 
"""
from rest_framework.decorators import api_view, authentication_classes, permission_classes # todo esto es para convertir un view normal en un api endpoint en el que solamente personas autenticadas pueden entrar
from .models import ChatSession
from .models import 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated 
from .serializers import SessionIdSerializer

# Defino la sesión afuera para que sea una variable global
session = None

# Esta función es estándar para las 6 funciones principales.
def handle_request(request, session, current_state, button, action, new_state=None, message=''):
    data = request.data
    if session.state == current_state and button == action.__name__:
        response = action(request, data)
        if new_state:
            session.state = new_state
            session.save()
        
        return Response({'message': message, 'state': session.state, 'response': response}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def decision_tree(request):
    data = request.data
    button = data.get('button')
    
    # Aquí estamos creando una nueva sesión por si pican el botón de create session
    if button == crear_sesion_chat:
        # Definimos el current session y el serializer de la función y luego lo mandamos de regreso al frontend. Así cuando un usuario cambie de un chat id a otro el backend también lo procesa. 
        session, serializer = crear_sesion_chat(request, data)
        return Response({'session_id': serializer.data}, status=status.HTTP_201_CREATED)

    # Aquí estamos cambiando el current session 
    if button == cambiar_sesion_chat:
        new_session_id = data.get('session_id')
        session = ChatSession.objects.get(session_id=new_session_id)

    # Cuando el usuario presione para mandar los datos del negocio, guardaremos sus datos relacionados a una sola sesión de chat. 
    # el flow en términos de botones es: mandar datos negocio -> guardar datos negocio o cambiar datos negocio -> idea
    response = handle_request(request, session, 'BUSINESS', button , mandar_datos_negocio, new_state='CHANGE_BUSINESS', message='Los datos del negocio se guardaron exitosamente en la base de datos.')
    if response:
        return response

    # Si el usuario presiona cambiar datos negocio, regresa al estado de business en donde tendrá la opción de volver a mandar sus datos. 
    response = handle_request(request, session, 'CHANGE_BUSINESS', button, cambiar_datos_negocio, new_state='BUSINESS', message='Los datos del negocio se cambiaron exitosamente')
    if response:
        return response

    # Si el usuario presiona para guardar los datos del negocio, entonces el estado se cambiará a idea. Ya guardamos los datos en la base de datos en mandar_datos_negocio, entonces no hay necesidad de volver a guardarlos aquí. 
    response = handle_request(request, session, 'CHANGE_BUSINESS', button, guardar_datos_negocio, new_state='IDEA', message='Los datos del negocio se guardaron exitosamente.')
    if response:
        return response

    # Esta función se encarga de crear la idea
    response = handle_request(request, session, 'IDEA', button, crear_idea, new_state='CHANGE_IDEA', message='La idea se creó exitosamente.')
    if response:
        return response

    # Aquí el usuario podrá tomar el feedback del usuario y gpt deberá guardarlo en su memoria para el resto de esta conversación 
    response = handle_request(request, session, 'CHANGE_IDEA', button, cambiar_idea, new_state='CHANGE_IDEA', message='La nueva idea se creó exitosamente.')
    if response:
        return response

    # Este botón es de transición, y su trabajo es continuar al siguente state
    response = handle_request(request, session, 'CHANGE_IDEA', button, guardar_idea, new_state='IMAGE', message='la idea se guardó exitosamente.')
    if response:
        return response

    # Esta función se encarga de crear la imagen
    response = handle_request(request, session, 'IMAGE', button, crear_imagen, new_state='CHANGE_IMAGE', message='La imagen se creó exitosamente.')
    if response:
        return response

    # Esta función se encarga de cambiar la imagen con el feedback del cliente con la memoria de gpt4 
    response = handle_request(request, session, 'CHANGE_IMAGE', button, cambiar_imagen, new_state='CHANGE_IMAGE', message='La nueva imagen se creó exitosamente.')
    if response:
        return response

    # Esta función es de transición, y su fin es continuar el state
    response = handle_request(request, session, 'CHANGE_IMAGE', button, guardar_imagen, new_state='CAPTION', message='La imagen se guardó a la base de datos exitosamente.')
    if response:
        return response

    # Esta función se encarga de crear el caption
    response = handle_request(request, session, 'CAPTION', button, crear_caption, new_state='CHANGE_CAPTION', message='La idea se creó exitosamente.')
    if response:
        return response

    # Esta función se encarga de cambiar el caption con el feedback del cliente con la memoria de gpt4 
    response = handle_request(request, session, 'CHANGE_CAPTION', button, cambiar_caption, new_state='CHANGE_CAPTION', message='El nuevo caption se creó exitosamente.')
    if response:
        return response

    # Esta función es de transición, y su fin es continuar el state
    response = handle_request(request, session, 'CHANGE_CAPTION', button, final, new_state='FINAL', message='La imagen se guardó a la base de datos exitosamente.')
    if response:
        return response


def crear_sesion_chat(request, data):
    new_session = ChatSession.objects.create(
        user=request.user,
        state='BUSINESS'
    )
    new_session.save()
    serializer = SessionIdSerializer(new_session)

    # Aquí mandamos la sesión de chat de regreso, así como los datos serializados para luego mandar el response 
    return new_session, serializer

def mandar_datos_negocio(request, data):

def guardar_datos_negocio(request, data):
    return null

def cambiar_datos_negocio(request, data):
    UserProfile.objects.create(
        user = request.user
        business_name = data.business_name
        business_description = data.business_description
        target_audience = data.target_audience
        image_style = data.image_style
    )

def crear_idea(request, data):

def cambiar_idea(request, data):

def guardar_idea(request, data):

def crear_imagen(request, data):

def cambiar_imagen(request, data):

def guardar_imagen(request, data):

def crear_caption(request, data):

def cambiar_caption(request, data):

def guardar_caption(request, data):

def final(request, data):