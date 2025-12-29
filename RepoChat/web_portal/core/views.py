from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Repository
import json
from django.contrib.auth.decorators import login_required
from forms import RepositoryForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
def chat_interface(request, repo_id):
    """
    Renders the chat page and handles message sending.
    """
    # Get the repository
    repo = get_object_or_404(Repository, id=repo_id)
    
    if request.method == "POST":
        try:
            # Get the message from the frontend
            data = json.loads(request.body)
            user_query = data.get('query')
            
            # Call the AI Engine (FastAPI) running on port 8001
            ai_response = requests.post(
                "http://127.0.0.1:8001/chat",
                json={
                    "repo_id": repo_id,
                    "query": user_query
                }
            )
            
            # Return the AI's answer to the frontend
            return JsonResponse(ai_response.json())
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # If it's a GET request, just show the empty chat page
    return render(request, 'chat.html', {'repo': repo})


# The Dashboard
@login_required
def dashboard(request):
    # Get all repos (In a real app, filter by user: Repository.objects.filter(user=request.user))
    repos = Repository.objects.all().order_by('-uploaded_at')
    return render(request, 'dashboard.html', {'repos': repos})

# Delete View
@login_required
def delete_repo(request, repo_id):
    repo = get_object_or_404(Repository, id=repo_id)
    if request.method == "POST":
        repo.delete()
        return redirect('dashboard')
    return render(request, 'web_portal/confirm_delete.html', {'repo': repo})


@login_required
def upload_repo(request):
    if request.method == 'POST':
        form = RepositoryForm(request.POST, request.FILES)
        if form.is_valid():
            if form.is_valid():
                print("Form is VALID. Saving...") # <--- DEBUG 2
                repo = form.save()
                print(f"Saved Repo ID: {repo.id}") # <--- DEBUG 3
            return redirect('dashboard')
        else:
            print(f"Form Errors: {form.errors}")       
            return redirect('dashboard')
    else:
        form = RepositoryForm()
    
    return render(request, 'upload.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after signing up
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


@login_required
def delete_repo(request, repo_id):
    # Get the repo (or show 404 if not found)
    repo = get_object_or_404(Repository, id=repo_id)

    if request.method == "POST":
        repo.delete()
        return redirect('dashboard')
    return render(request, 'confirm_delete.html', {'repo': repo})