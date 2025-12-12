from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Define Priority levels as a list of 2-tuples (database_value, human_readable_name)
PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MED', 'Medium'),
        ('HIGH', 'High'),
    ]

# Define Status levels as a list of 2-tuples
STATUS_CHOICES = [
        ('PEND', 'Pending'),
        ('COMP', 'Completed'),
    ]

"""class - Category schema"""
class Category(models.Model):
    categ_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.categ_name
    
class Meta:
    verbose_name_plural = "Categories"

    def __str__(self):
        return self.verbose_name_plural
    

"""class - Task schema"""
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True)
    
    """ Data Fields """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=4,
        choices=PRIORITY_CHOICES,
        default='MED'       # Default value will be 'low'
    )
    status = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default='PEND'       # Default value will be 'pending'
    )
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Meta:
    ordering = ['-due_date']