from django.db import models
from django.db.models.fields import related

class User(models.Model):
    email        = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=100, unique=True, null=True)
    name         = models.CharField(max_length=100)
    nickname     = models.CharField(max_length=100, unique=True)
    password     = models.CharField(max_length=200)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Follow(models.Model):
    follower  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    
    class Meta:
        db_table = 'follows'