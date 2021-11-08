from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User)
