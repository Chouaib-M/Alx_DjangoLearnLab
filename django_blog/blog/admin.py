from django.contrib import admin
from .models import Post, UserProfile, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    search_fields = ("title", "content", "author__username")
    list_filter = ("published_date", "author")
    date_hierarchy = "published_date"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "date_joined", "bio")
    search_fields = ("user__username", "user__email", "bio")
    list_filter = ("date_joined",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at", "updated_at")
    search_fields = ("content", "author__username", "post__title")
    list_filter = ("created_at", "updated_at", "author")
    date_hierarchy = "created_at"
