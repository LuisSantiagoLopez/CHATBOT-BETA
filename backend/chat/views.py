from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import logging

@api_view(['POST'])
def user_signup(request):
    try:
        # Extracting username and password from the incoming request
        username = request.data['username']
        password = request.data['password']
        
        # Checking if a user with this username already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # If not, create a new user and token
        user = User.objects.create_user(username=username, password=password)
        token = Token.objects.create(user=user)
        
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        
    except IntegrityError as e:
        # This will catch any IntegrityError exceptions, including unique constraint violations
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # This will catch any other type of exceptions and log them
        logging.exception("Exception in user_signup: ")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""@api_view(['POST'])
def user_signup(request):
    print("Request Data:", request.data)
    username = request.data.get('username', None)
    password = request.data.get('password', None)

    if username is None or password is None:
        return Response({"error": "Username or password not provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, password=password)
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print("Exception:", e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
"""

@api_view(['POST'])
def user_login(request):
    username = request.data['username']
    password = request.data['password']
    
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            response = Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
            response.set_cookie('auth_token', token.key, httponly=True)
            return response
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response(status=status.HTTP_401_UNAUTHORIZED)