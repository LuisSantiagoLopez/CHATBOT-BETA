# Probablemente sea buena idea darle una checada a la documentación de django rest framework "https://www.django-rest-framework.org/tutorial/quickstart/" y alguna guía que te sea útil en internet.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, UserProfileSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail 
from .models import EmailVerificationToken
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate

# Esta view está conectada con el frontend en frontend->src->components->signup
# Esta view es para registrar a los usuarios.  
class RegisterUserAPIView(APIView):
    # Esta función maneja las request tipo post
    def post(self, request):
        # Definimos el serializer con el que django validará la información que proviene del frontend, covertirá los datos de json a python, y los guardará en la base de datos.
        serializer = RegisterUserSerializer(data=request.data) # Le indicamos que los datos que va a verificar. 
        if serializer.is_valid(): 
            # Si los datos son válidos, checamos si el email existe en la base de datos, si existe, regresamos el error. 
            email = serializer.validated_data['email'] # Si te fijas extraemos la información del serializer en vez del request
            if User.objects.filter(email=email).exists():
                return Response({"message": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save() #Esto llama a la función create() dentro del serializer y salva la información 

            """
            Todo el código comentado no sirve, lo que intenté hacer es crear un token en los modelos, y luego mandar un mail de confirmación. 

            user.is_active=False

            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            # Create a unique email verification token and save it
            email_token = EmailVerificationToken.objects.create(user=user)

            # Send an email with the verification link
            send_mail(
                'Email Verification',
                f'Click the link to verify your email: http://localhost:3000/verify-email/{email_token.token}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            """

            return Response({"message": "User created. Please verify your email.", "token": token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # EXPECTED OUTPUT: usuario registrado en el backend, con el teléfono celular verificado y con un captcha completado. 
        # Lo del teléfono y captcha te puede parecer mucho, pero solo es para que (1) no abusen tanto del freemium porque es más difícil tener más de un número de teléfono que más de un gmail, (2) tengamos algún protocolo de seguridad


# Esta función no sirve, toda esta parte la hizo ChatGPT y la hizo mal. No te sientas mal en borrarla.
# En verdad lo que quería era verificar su número de teléfono. Para esto tendrás que añadir teléfono en los models, añadirlo a los serializers, y yo ponerlo en el frontend. Quiero que no puedan tener acceso a nada hasta que verifiquen su teléfono. Recuerda pensar de esto del modo más simple y sencillo posible. 
class VerifyEmailAPIView(APIView):
    def get(self, request, token):
        try:
            email_token = EmailVerificationToken.objects.get(token=token)

            # Check if token has expired (e.g., after 24 hours)
            if timezone.now() > email_token.created_at + timedelta(hours=24):
                return Response({"message": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)

            # Mark the email as verified
            email_token.user.is_email_verified = True
            email_token.user.save()

            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)

        except EmailVerificationToken.DoesNotExist:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            #EXPECTED OUTPUT: un

# Esta view está conectada con el frontend en frontend->src->components->login
# Esta se supone que es la view para hacer login, sin embargo, me dijiste que hay un método llamado login. Esta función también la hizo ChatGPT
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        # EXPECTED OUTPUT: Que el usuario pueda hacer login automático o manualmente

# Esta view está conectada con el frontend en frontend->src->app.js
class LogoutAPIView(APIView):
    def post(self, request):
        request.auth.delete()
        # Acá borramos el auth, pero como me comentaste, crees que esto es mala idea 
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        # Que el usuario haga logout 

# Esta view está conectada con el frontend en frontend->src->profile. Sirve para que los usuarios puedan ver su información del login. 
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

# La mayoría de lo que escribí es basura. La única cosa importante es que el api ya está conectado.