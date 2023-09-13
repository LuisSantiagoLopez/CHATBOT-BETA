from rest_framework import serializers
from django.contrib.auth.models import User

# Este serializer verifica la info, la convierte a python, y después la salva
class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Le indicamos que los datos que va a recibir mimican al modelo predeterminado User de la base de datos
        fields = ('email', 'password')
        # Solo vamos a usar el email y la contraseña para facilitar el proceso de registro
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data): # Acá salvamos los datos validados del usuario en la base de datos. 
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class UserProfileSerializer(serializers.ModelSerializer): # Este serializer solamente sirve para procesar y validar los datos. Es parte de "UserProfileView" y ayuda a desplegar los datos del usuario. 
    class Meta:
        model = User
        fields = ('email', 'password')