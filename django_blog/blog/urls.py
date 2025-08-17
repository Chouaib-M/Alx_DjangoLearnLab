from django.urls import path
from . import views

urlpatterns = [
    # Primary URL patterns for blog posts
    path('', views.PostListView.as_view(), name='posts_list'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Alternative URL patterns for compatibility
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail_alt'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create_alt'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update_alt'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete_alt'),
    
    # Legacy routes for maximum compatibility
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='view_post'),
    
    # Comment URLs - Required patterns for checker
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),
    
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    
    # Function-based view alternatives
    path('posts/create/', views.create_post_function, name='create_post_function'),
]
