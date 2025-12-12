from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # API Routs
    path('tasks/', views.task_collection, name='task-list'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'),
    path('categories/', views.category_list, name='category-list'),
]