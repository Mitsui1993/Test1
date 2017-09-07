from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=32)

class Role(models.Model):
    name = models.CharField(max_length=32)
