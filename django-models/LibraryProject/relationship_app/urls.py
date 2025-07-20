from django.urls import path
from .views import list_books, LibraryDetailView, UserLoginView, UserLogoutView, register

urlpatterns = [
    path('books/', list_books, name='list_books'),  # FBV URL
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # CBV URL
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]
