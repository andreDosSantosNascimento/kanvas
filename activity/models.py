from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Submission(models.Model):
    grade = models.IntegerField(null=True)
    repo = models.CharField(max_length=255)
    user_id = models.IntegerField()
    activity_id = models.IntegerField()


class Activity(models.Model):
    title = models.CharField(max_length=255, unique=True)
    points = models.IntegerField(User)
    submissions = models.ManyToManyField(Submission)
