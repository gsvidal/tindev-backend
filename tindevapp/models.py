from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
  id = models.AutoField(primary_key=True)
  USER_ROLES = [
        ("Dev", "Dev"),
        ("Recruiter", "Recruiter"),
    ]
  role = models.CharField(max_length=10, choices=USER_ROLES, default="Dev")
  created_at = models.DateTimeField(default=timezone.now)


class Dev(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)


class Recruiter(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  isIndependent = models.BooleanField(default=True)
  company_name = models.CharField(max_length=20)