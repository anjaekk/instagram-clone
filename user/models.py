from django.db import models

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