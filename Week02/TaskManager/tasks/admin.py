from django.contrib import admin
from .models import Task, Category

class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'priority', 
        'status', 
        'category', 
        'due_date', 
        'user'
    )

    # --- Sidebar Filters (list_filter) ---
    # Adds a sidebar to filter results by these specific fields
    list_filter = (
        'status', 
        'priority', 
        'category'
    )

    # --- Search Bar (search_fields) ---
    # Adds a search bar that searches within these text fields
    search_fields = (
        'title', 
        'description'
    )

# Register your models here.
admin.site.register(Category)
admin.site.register(Task, TaskAdmin)