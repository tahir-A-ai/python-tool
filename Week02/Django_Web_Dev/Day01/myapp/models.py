from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class RegisterUser(models.Model):
    roles = [
        ('std', 'Student'),
        ('teach', 'Teacher')
    ]
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Myimgs/")
    registration_date = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=5, choices=roles)

    def __str__(self):
        return self.name
