from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    
    # User discovery
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    
    # Follow functionality
    path('follow/<int:user_id>/', views.follow_user, name='follow-user'),
]
