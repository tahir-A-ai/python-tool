from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect   # create ORM layer to Talk to DB
from .models import Tweet
from .forms import TweetForms, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request, 'index.html')

# fetching tweets list from DB
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

# Create new Tweet
@login_required
def create_tweet(request):
    if request.method == "POST":
        form = TweetForms(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False) #commit=False > not saving to DB for now as we also need user ho sent this tweet
            # getting user as well from request body
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForms()
        return render(request, 'tweet_form.html', {'form':form})
    
# Edit Tweet
@login_required
def edit_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == "POST":
        form = TweetForms(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForms(instance=tweet)
    return render(request, 'tweet_form.html', {'form':form})

# Delete Tweet
@login_required
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == "POST":
        tweet.delete()  # >> Here validting form is optional
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_deletion.html', {'tweet':tweet})

def resgister(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render (request, 'registration/register.html', {'form':form})