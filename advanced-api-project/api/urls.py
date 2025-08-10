from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Author endpoints
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # Book endpoints
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Test endpoint
    path('test/', views.test_serializers, name='test-serializers'),
] 