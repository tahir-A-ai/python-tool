from django.shortcuts import render
from .models import RegisterUser

# Create your views here.
def myapphome(request):
    users = RegisterUser.objects.all()
    return render(request, 'myapp.html', {'users':users})
