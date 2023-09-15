from django.db import models  # Importing Django's models module to define our model classes
from user_management.models import UserProfile  # Importing UserProfile model to make a ForeignKey relation
import random
from django.contrib.auth.models import User 
from django.db.models.signals import pre_save
from django.dispatch import receiver 

# Model for tracking individual chat sessions
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.IntegerField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Stores the time when the session was created
    state = models.CharField(  # The current state in the decision tree ('IDEA', 'IMAGE', 'CAPTION')
        max_length=30,
        choices=[('BUSINESS', 'Business'), ('CHANGE_BUSINESS', 'Change_Business'), ('IDEA', 'Idea'), ('CHANGE_IDEA', 'Change_Idea'), ('IMAGE', 'Image'), ('CHANGE_IMAGE', 'Change_Image'), ('CAPTION', 'Caption'), ('CHANGE_CAPTION', 'Change_Caption'), ('FINAL', 'Final')],
        default='BUSINESS'
    )
    
# Signal to generate a unique session_id before saving
@receiver(pre_save, sender=ChatSession)
def generate_unique_session_id(sender, instance, **kwargs):
    if instance.session_id is None:  # Only generate if it's not already set
        instance.session_id = random.randint(1000, 9999)
        
        # Check for uniqueness, and regenerate if needed
        while ChatSession.objects.filter(session_id=instance.session_id).exists():
            instance.session_id = random.randint(1000, 9999)

class BusinessDetails(models.Model):
    chat_session = models.OneToOneField(ChatSession, on_delete=models.CASCADE, related_name='business_details')
    business_name = models.TextField(null=True, blank=True)
    business_description = models.TextField(null=True, blank=True)
    target_audience = models.TextField(null=True, blank=True)
    writing_style = models.TextField(null=True, blank=True)
    image_style = models.TextField(null=True, blank=True)


# Model for tracking all messages in a chat session
class ChatLog(models.Model):
    SESSION_TYPE_CHOICES = [  # Choices for the type of message (System-generated, User, or AI)
        ('SYSTEM', 'System'),
        ('USER', 'User'),
        ('AI', 'AI'),
    ]
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)  # GPT4 deberá tener memoria de cada sesión. Igual que en chatgpt tienen que haber distintas conversaciones. 
    message_type = models.CharField(max_length=10, choices=SESSION_TYPE_CHOICES)  # Type of the message
    message_content = models.TextField()  # Content of the message
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the message was sent
    related_idea = models.ForeignKey('Idea', null=True, blank=True, on_delete=models.SET_NULL)  # Link to the related idea if any
    related_image = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL)  # Link to the related image if any
    related_caption = models.ForeignKey('Caption', null=True, blank=True, on_delete=models.SET_NULL)  # Link to the related caption if any

# Model for holding generated ideas
class Idea(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)  # Linking each idea to a session
    text = models.TextField()  # The text content of the idea
    chosen = models.BooleanField(default=False)  # Whether the idea was chosen by the user or not
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the idea was generated

# Model for holding generated images
class Image(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)  # Linking each image to a session
    image_url = models.URLField()  # The URL of the generated image
    chosen = models.BooleanField(default=False)  # Whether the image was chosen by the user or not
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the image was generated

# Model for holding generated captions
class Caption(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)  # Linking each caption to a session
    text = models.TextField()  # The text content of the caption
    chosen = models.BooleanField(default=False)  # Whether the caption was chosen by the user or not
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the caption was generated
