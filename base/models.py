from django.db import models
# # Create your models here. 
from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     name = models.CharField(max_length=200, null=True)
#     email = models.EmailField(null=True, unique=True)
#     bio=models.TextField(null=True)
#     avatar = models.ImageField(null=True, default="avatar.jpeg")

#     USERNAME_FIELD='email'
#     REQUIRED_FIELDS=[]

import cloudinary
import cloudinary.models

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, unique=True)
    bio = models.TextField(null=True)
    avatar = cloudinary.models.CloudinaryField('avatar', default='avatar.jpeg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=252)

    def __str__(self):
        return self.name


class Room(models.Model):
    host= models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    topic= models.ForeignKey(Topic, on_delete=models.SET_NULL, null= True)
    name = models.CharField(max_length=252)
    likes = models.IntegerField(default=0)
    likedBy = models.ManyToManyField(User, related_name='likers')
    participants = models.ForeignKey(User, related_name='participants', on_delete=models.SET_NULL, null= True)
    description = models.TextField(null=True, blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [ '-created','-likes' ] 

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body=models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body

