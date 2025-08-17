from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, UserProfile
from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm


def home(request):
    posts = Post.objects.select_related('author').order_by('-published_date')[:10]
    context = {
        'posts': posts,
        'user': request.user
    }
    return render(request, 'blog/home.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Django Blog!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    user_form = None
    profile_form = None
    
    if request.method == 'POST':
        # Check which form was submitted
        if 'update_user' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your user information has been updated successfully!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors in user information.')
        elif 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors in profile information.')
    
    # Initialize forms if not already set
    if user_form is None:
        user_form = UserUpdateForm(instance=request.user)
    if profile_form is None:
        profile_form = UserProfileForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': request.user
    }
    return render(request, 'registration/profile.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            Post.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            messages.success(request, 'Post created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'blog/create_post.html')
