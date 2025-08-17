from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.home, name='posts'),
    path('register/', views.register, name='register'),
]


