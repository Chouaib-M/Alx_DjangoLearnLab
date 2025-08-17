from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    """
    Blog Post model for managing blog posts with CRUD operations.
    This model supports the blog post management features including:
    - Creating new posts (authenticated users only)
    - Reading posts (all users)
    - Updating posts (author only via LoginRequiredMixin and UserPassesTestMixin)
    - Deleting posts (author only via LoginRequiredMixin and UserPassesTestMixin)
    """
    title = models.CharField(max_length=200, help_text="Title of the blog post")
    content = models.TextField(help_text="Main content of the blog post")
    published_date = models.DateTimeField(auto_now_add=True, help_text="Date and time when post was created")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', 
                              help_text="Author of the post - used for permission checks")
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', 
                                 help_text="Tags associated with this post")

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['-published_date']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"


class Comment(models.Model):
    """
    Comment model for blog post comments.
    Allows users to comment on blog posts with full CRUD functionality.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',
                           help_text="The blog post this comment belongs to")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments',
                             help_text="The user who wrote this comment")
    content = models.TextField(help_text="The comment text content")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the comment was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the comment was last updated")

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Tag(models.Model):
    """
    Tag model for categorizing blog posts.
    Allows many-to-many relationship with posts for flexible tagging.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Tag name")
    slug = models.SlugField(max_length=100, unique=True, help_text="URL-friendly tag name")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
