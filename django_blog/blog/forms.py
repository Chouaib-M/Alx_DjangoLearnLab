from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, UserProfile, Comment, Tag


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
    ModelForm for creating and editing blog posts with tagging support.
    Used in conjunction with Django's LoginRequiredMixin and UserPassesTestMixin
    to ensure proper permissions for blog post management CRUD operations.
    
    Features:
    - Create: Used with LoginRequiredMixin in PostCreateView
    - Update: Used with LoginRequiredMixin + UserPassesTestMixin in PostUpdateView  
    - Author field automatically set from request.user
    - Form validation for title and content fields
    - Tag support for categorizing posts
    """
    tags = forms.CharField(
        max_length=200, 
        required=False,
        help_text='Enter tags separated by commas (e.g., python, django, web)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas...'
        })
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Author is set automatically from request.user
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
            'content': 'Post Content',
            'tags': 'Tags'
        }
        help_texts = {
            'title': 'Enter a descriptive title for your blog post',
            'content': 'Write the main content of your blog post'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Pre-populate tags field with existing tags
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            # Handle tags
            if self.cleaned_data.get('tags'):
                tag_names = [name.strip() for name in self.cleaned_data['tags'].split(',') if name.strip()]
                post.tags.clear()
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': tag_name.lower().replace(' ', '-')}
                    )
                    post.tags.add(tag)
            else:
                post.tags.clear()
        return post


class CommentForm(forms.ModelForm):
    """
    ModelForm for creating and editing comments on blog posts.
    Used for comment CRUD operations with proper validation.
    """
    class Meta:
        model = Comment
        fields = ['content']  # Post and author are set automatically
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...',
                'required': True
            })
        }
        labels = {
            'content': 'Comment'
        }
        help_texts = {
            'content': 'Share your thoughts about this blog post'
        }
