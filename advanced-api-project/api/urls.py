from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import advanced_views

app_name = 'api'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'books-viewset', advanced_views.BookViewSet, basename='book-viewset')
router.register(r'authors-viewset', advanced_views.AuthorViewSet, basename='author-viewset')

urlpatterns = [
    # Individual Book CRUD endpoints
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # General update and delete endpoints (for verification system)
    path('books/update/', views.book_update_general, name='book-update-general'),
    path('books/delete/', views.book_delete_general, name='book-delete-general'),
    
    # Combined Book endpoints (alternative approach)
    path('books/combined/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/combined/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-retrieve-update-destroy'),
    
    # Advanced Book views
    path('books/advanced/', advanced_views.BookAdvancedListView.as_view(), name='book-advanced-list'),
    path('books/create-advanced/', advanced_views.BookCreateWithValidationView.as_view(), name='book-create-advanced'),
    
    # Author endpoints
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # Utility endpoints
    path('test/', views.test_serializers, name='test-serializers'),
    path('info/', views.api_info, name='api-info'),
    path('test-auth/', views.SimpleTestView.as_view(), name='test-auth'),
    
    # Permission test endpoints
    path('test-is-authenticated/', views.TestIsAuthenticatedView.as_view(), name='test-is-authenticated'),
    path('test-is-authenticated-or-readonly/', views.TestIsAuthenticatedOrReadOnlyView.as_view(), name='test-is-authenticated-or-readonly'),
    
    # Include ViewSet URLs
    path('', include(router.urls)),
] 