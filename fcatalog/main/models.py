from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email


class Discipline(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    approved_date = models.DateTimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
