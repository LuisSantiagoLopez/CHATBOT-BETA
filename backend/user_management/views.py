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


class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                return Response({"message": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
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

            return Response({"message": "User created. Please verify your email.", "token": token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self, request):
        request.auth.delete()
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user