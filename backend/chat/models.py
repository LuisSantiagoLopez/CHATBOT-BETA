from django.db import models  # Importing Django's models module to define our model classes
from user_management.models import UserProfile  # Importing UserProfile model to make a ForeignKey relation

# Model for tracking individual chat sessions
class ChatSession(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Linking each session to a user profile
    created_at = models.DateTimeField(auto_now_add=True)  # Stores the time when the session was created
    state = models.CharField(  # The current state in the decision tree ('IDEA', 'IMAGE', 'CAPTION')
        max_length=15,
        choices=[('IDEA', 'Idea'), ('IMAGE', 'Image'), ('CAPTION', 'Caption')],
        default='IDEA'
    )
    decision_tree_state = models.JSONField(null=True)  # Dynamic field to store the state of the decision tree for more complex flows

# Model for tracking all messages in a chat session
class ChatLog(models.Model):
    SESSION_TYPE_CHOICES = [  # Choices for the type of message (System-generated, User, or AI)
        ('SYSTEM', 'System'),
        ('USER', 'User'),
        ('AI', 'AI'),
    ]
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)  # Linking each message to a chat session
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
