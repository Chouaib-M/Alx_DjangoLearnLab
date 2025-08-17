from django.urls import path
from . import views

urlpatterns = [
    # Home and Posts
    path('', views.home, name='home'),
    path('posts/', views.PostListView.as_view(), name='posts_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # CRUD Operations for Posts
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Legacy routes (kept for compatibility)
    path('create-post/', views.create_post, name='create_post'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]


