from django.db import models  # Importing Django's models module to define our model classes
from user_management.models import UserProfile  # Importing UserProfile model to make a ForeignKey relation
import random
from django.contrib.auth.models import User 
from django.db.models.signals import pre_save
from django.dispatch import receiver 

# Modelo para crear una sesión de chat 
class ChatSession(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    session_id = models.IntegerField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Momento en el que se creó la sesión 
    state = models.CharField(  # El estado en el que está la sesión de chat. De esto depende cómo cambia el frontend.  
        max_length=30,
        choices=[('BUSINESS', 'Business'), ('CHANGE_BUSINESS', 'Change_Business'), ('IDEA', 'Idea'), ('CHANGE_IDEA', 'Change_Idea'), ('IMAGE', 'Image'), ('CHANGE_IMAGE', 'Change_Image'), ('CAPTION', 'Caption'), ('CHANGE_CAPTION', 'Change_Caption'), ('FINAL', 'Final')],
        default='BUSINESS'
    )
    
# Esta señal prácticamente dice "antes de salvar cada sesión, crea un ID"
@receiver(pre_save, sender=ChatSession)
def generate_unique_session_id(sender, instance, **kwargs):
    if instance.session_id is None:  # Solo genera uno si no existe. 
        instance.session_id = random.randint(1000, 9999)
        
        # Revisa que sea único 
        while ChatSession.objects.filter(session_id=instance.session_id).exists():
            instance.session_id = random.randint(1000, 9999)

# Estos son los elementos que el LLM usará para generar. 
class BusinessDetails(models.Model):
    chat_session = models.OneToOneField(ChatSession, on_delete=models.CASCADE, related_name='business_details')
    business_name = models.TextField(null=True, blank=True)
    business_description = models.TextField(null=True, blank=True)
    target_audience = models.TextField(null=True, blank=True)
    writing_style = models.TextField(null=True, blank=True)
    image_style = models.TextField(null=True, blank=True)


# Modelo para trackear la conversaciónd de cada chat. 
class ChatLog(models.Model):
    SESSION_TYPE_CHOICES = [  # Choices for the type of message (System-generated, User, or AI)
        ('USER', 'User'),
        ('AI', 'AI'),
    ]
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)  # GPT4 deberá tener memoria de cada sesión. Igual que en chatgpt tienen que haber distintas conversaciones. 
    message_type = models.CharField(max_length=10, choices=SESSION_TYPE_CHOICES)  # Tipo de mensaje
    message_content = models.TextField()  # Contenido del mensaje
    timestamp = models.DateTimeField(auto_now_add=True)  # Momento en el que mandé el mensaje

# Modelo que guarda las ideas.
class Idea(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)  # Linking each idea to a session
    idea = models.TextField()  # The text content of the idea
    chosen = models.BooleanField(default=False)  # Si la idea está activa en este momento 
    approved = models.BooleanField(default=False) # Esto nos servirá para entrenar los modelos más adelante 
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the idea was generated

# Modelo para guardar las imágenes 
class Image(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)  # Haciendo link entre la idea y la sesión 
    image_prompt = models.TextField()
    image_url = models.URLField()  # El URL de la imagen generada 
    chosen = models.BooleanField(default=False)  # Si la imagen está activa en este momento
    approved = models.BooleanField(default=False) # Esto nos servirá para entrenar los modelos más adelante 
    timestamp = models.DateTimeField(auto_now_add=True)  # Tiempo en el que la imagen fue generada 

# Modelo para guardar un caption 
class Caption(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)  # Haciendo link entre la caption y la sesión 
    text = models.TextField()  # El contenido de la caption 
    chosen = models.BooleanField(default=False)  # Si el usuario usó el caption 
    approved = models.BooleanField(default=False) # Esto nos servirá para entrenar los modelos más adelante 
    timestamp = models.DateTimeField(auto_now_add=True)  # Momento en el que se generó el caption 

# Este modelo guarda una publicación entera en la base de datos para poder enseñársela después al usuario. Falta desarrollar esta parte 
class UserPost(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    idea = models.OneToOneField(Idea, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.OneToOneField(Image, on_delete=models.SET_NULL, null=True, blank=True)
    caption = models.OneToOneField(Caption, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)