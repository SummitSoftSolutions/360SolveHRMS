import uuid
from django.db import models

# Create your models here.
class SuperAdmin(models.Model):
    Name=models.CharField(max_length=150)
    email =models.EmailField(unique=True)
    Password = models.CharField(max_length=150)
    
    def __str__(self):
        return self.Name


