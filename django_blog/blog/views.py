from django.shortcuts import render
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


def home(request):
    posts = Post.objects.select_related('author').order_by('-published_date')[:10]
    return render(request, 'blog/home.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Create your views here.
