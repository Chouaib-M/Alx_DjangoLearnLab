from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.create(user=user)
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class PostForm(forms.ModelForm):
    """
    ModelForm for creating and editing blog posts.
    Used in conjunction with Django's LoginRequiredMixin and UserPassesTestMixin
    to ensure proper permissions for blog post management CRUD operations.
    
    Features:
    - Create: Used with LoginRequiredMixin in PostCreateView
    - Update: Used with LoginRequiredMixin + UserPassesTestMixin in PostUpdateView  
    - Author field automatically set from request.user
    - Form validation for title and content fields
    """
    class Meta:
        model = Post
        fields = ['title', 'content']  # Author is set automatically from request.user
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your post content here...',
                'required': True
            })
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content'
        }
        help_texts = {
            'title': 'Enter a descriptive title for your blog post',
            'content': 'Write the main content of your blog post'
        }
