from django.db import models
from users.models import User

# django-ckeditor
from ckeditor.fields import RichTextField

class Movies(models.Model):
    gender_choices = [
        ('AC', 'Action'),
        ('SE', 'Serie'),
        ('AD', 'Adventure'),
        ('DR', 'Drama'),
        ('CO', 'Comedy'),
        ('SU', 'Suspended'),
        ('CR', 'Crime'),
        ('TE', 'Terror'),
        ('AN', 'Animation'),
        ('SF', 'Science fiction'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=2, choices=gender_choices)
    author = models.CharField(max_length=30)
    production = models.CharField(max_length=30)
    image = models.ImageField(null=True, upload_to='movies')
    duration = models.DurationField()
    date_launch = models.DateField()
    description = RichTextField(null=True)

    def __str__(self):
        return f'{self.name}'
