from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    modified = models.DateTimeField(auto_now=True)
    photo = models.ImageField(null=True, upload_to='users')
    about = RichTextField(null=True)
    phone = models.CharField(null=True, max_length=15)
    city = models.CharField(null=True, max_length=255)
    country = models.CharField(null=True, max_length=255)