from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  ROLES = [
    ('therapist','Therapist'),
    ('student','Student'),
    ('staff','Staff'),
  ]
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
  role = models.CharField(max_length=255,choices=ROLES)
  image= models.CharField(max_length=255,null=True,blank=True)
  
  # for students and staff
  department= models.CharField(max_length=255,null=True,blank=True)
  
  # for therapists
  level_of_education = models.CharField(max_length=255,null=True,blank=True)
  document = models.CharField(max_length=255,null=True,blank=True)
  
class ChatRoom(models.Model):
  users = models.ManyToManyField(
    User,
    through="ChatRoomUser",
    related_name="chat_rooms"
  )
  admin = models.ForeignKey(User,on_delete=models.CASCADE)
  lastMessage = models.ForeignKey('Message',on_delete=models.CASCADE,null=True,blank=True)
  
  is_private = models.BooleanField(default=False)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.users.only('username')}"
  
class ChatRoomUser(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  chatRoom = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
  joined_at = models.DateTimeField(auto_now_add=True)
  
class Message(models.Model):
  sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_messages")
  chatRoom = models.ForeignKey(ChatRoom,on_delete=models.CASCADE,related_name="chat_messages")
  content = models.TextField()
  sent_at = models.DateTimeField(auto_now_add=True)
  