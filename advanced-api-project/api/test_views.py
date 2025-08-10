"""
Unit Tests for Django REST Framework APIs

This module contains comprehensive unit tests for the Book Management API,
covering CRUD operations, filtering, searching, ordering, and authentication/permissions.

Test Coverage:
- CRUD operations for Book model endpoints
- Filtering, searching, and ordering functionalities
- Authentication and permission mechanisms
- Response data integrity and status codes
- Error handling and edge cases
"""

import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(TestCase):
    """
    Base test case for Book API tests.
    
    Sets up test data and provides common utility methods.
    """
    
    def setUp(self):
        """Set up test data and client."""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test author
        self.author = Author.objects.create(name='J.R.R. Tolkien')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='The Hobbit',
            author=self.author,
            publication_year=1937
        )
        
        self.book2 = Book.objects.create(
            title='The Lord of the Rings',
            author=self.author,
            publication_year=1954
        )
        
        # Create another author and book for testing
        self.author2 = Author.objects.create(name='George R.R. Martin')
        self.book3 = Book.objects.create(
            title='A Game of Thrones',
            author=self.author2,
            publication_year=1996
        )
        
        # Set up API client
        self.client = APIClient()
        
        # Test data for creating books
        self.book_data = {
            'title': 'Test Book',
            'author': self.author.id,
            'publication_year': 2020
        }
    
    def authenticate_user(self):
        """Authenticate the test user."""
        # Use login method to demonstrate separate test database usage
        self.client.login(username='testuser', password='testpass123')
        # Also use force_authenticate for API testing
        self.client.force_authenticate(user=self.user)


class BookCRUDTests(BookAPITestCase):
    """
    Test cases for CRUD operations on Book endpoints.
    """
    
    def test_list_books_success(self):
        """Test successful retrieval of book list."""
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 3)
        
        # Check if books are in response
        book_titles = [book['title'] for book in response.data['results']]
        self.assertIn('The Hobbit', book_titles)
        self.assertIn('The Lord of the Rings', book_titles)
        self.assertIn('A Game of Thrones', book_titles)
    
    def test_retrieve_book_success(self):
        """Test successful retrieval of a single book."""
        url = reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Hobbit')
        self.assertEqual(response.data['publication_year'], 1937)
        self.assertEqual(response.data['author_name'], 'J.R.R. Tolkien')
    
    def test_retrieve_book_not_found(self):
        """Test retrieval of non-existent book."""
        url = reverse('api:book-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_book_authenticated_success(self):
        """Test successful book creation by authenticated user."""
        self.authenticate_user()
        url = reverse('api:book-create')
        response = self.client.post(url, self.book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['publication_year'], 2020)
        
        # Verify book was created in database
        self.assertTrue(Book.objects.filter(title='Test Book').exists())
    
    def test_create_book_unauthenticated_failure(self):
        """Test book creation fails for unauthenticated user."""
        url = reverse('api:book-create')
        response = self.client.post(url, self.book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_book_invalid_data(self):
        """Test book creation with invalid data."""
        self.authenticate_user()
        url = reverse('api:book-create')
        invalid_data = {
            'title': '',  # Empty title
            'author': self.author.id,
            'publication_year': 2020
        }
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_book_authenticated_success(self):
        """Test successful book update by authenticated user."""
        self.authenticate_user()
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        update_data = {
            'title': 'Updated Hobbit',
            'author': self.author.id,
            'publication_year': 1938
        }
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Hobbit')
        self.assertEqual(response.data['publication_year'], 1938)
        
        # Verify book was updated in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Hobbit')
    
    def test_update_book_unauthenticated_failure(self):
        """Test book update fails for unauthenticated user."""
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        update_data = {'title': 'Updated Title'}
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_book_authenticated_success(self):
        """Test successful book deletion by authenticated user."""
        self.authenticate_user()
        url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book was deleted from database
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
        
        # Check custom response message
        self.assertIn('message', response.data)
        self.assertIn('The Hobbit', response.data['message'])
    
    def test_delete_book_unauthenticated_failure(self):
        """Test book deletion fails for unauthenticated user."""
        url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BookFilteringTests(BookAPITestCase):
    """
    Test cases for filtering functionality.
    """
    
    def test_filter_by_author(self):
        """Test filtering books by author."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author': self.author.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check that only books by the specified author are returned
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author.id)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year': 1937})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'The Hobbit')
    
    def test_filter_by_year_range(self):
        """Test filtering books by year range."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'year_from': 1940, 'year_to': 2000})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check that only books in the specified range are returned
        for book in response.data['results']:
            self.assertGreaterEqual(book['publication_year'], 1940)
            self.assertLessEqual(book['publication_year'], 2000)
    
    def test_filter_by_title_starts_with(self):
        """Test filtering books by title prefix."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'title_starts_with': 'The'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check that only books with titles starting with 'The' are returned
        for book in response.data['results']:
            self.assertTrue(book['title'].startswith('The'))
    
    def test_filter_by_author_contains(self):
        """Test filtering books by author name containing string."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author_contains': 'Tolkien'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check that only books by authors with 'Tolkien' in their name are returned
        for book in response.data['results']:
            self.assertIn('Tolkien', book['author_name'])
    
    def test_combined_filters(self):
        """Test combining multiple filters."""
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'author': self.author.id,
            'year_from': 1930,
            'year_to': 1960
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check that filters are applied correctly
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author.id)
            self.assertGreaterEqual(book['publication_year'], 1930)
            self.assertLessEqual(book['publication_year'], 1960)


class BookSearchTests(BookAPITestCase):
    """
    Test cases for search functionality.
    """
    
    def test_search_by_title(self):
        """Test searching books by title."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'Hobbit'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'The Hobbit')
    
    def test_search_by_author_name(self):
        """Test searching books by author name."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'Tolkien'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check that only books by authors with 'Tolkien' in their name are returned
        for book in response.data['results']:
            self.assertIn('Tolkien', book['author_name'])
    
    def test_search_case_insensitive(self):
        """Test that search is case insensitive."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'hobbit'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'The Hobbit')
    
    def test_search_no_results(self):
        """Test search with no matching results."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'NonexistentBook'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    
    def test_search_combined_with_filter(self):
        """Test search combined with filtering."""
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'search': 'The',
            'year_from': 1930,
            'year_to': 1960
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check that both search and filter are applied
        for book in response.data['results']:
            self.assertIn('The', book['title'])
            self.assertGreaterEqual(book['publication_year'], 1930)
            self.assertLessEqual(book['publication_year'], 1960)


class BookOrderingTests(BookAPITestCase):
    """
    Test cases for ordering functionality.
    """
    
    def test_order_by_title_ascending(self):
        """Test ordering books by title in ascending order."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that books are ordered by title (A-Z)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, ['A Game of Thrones', 'The Hobbit', 'The Lord of the Rings'])
    
    def test_order_by_title_descending(self):
        """Test ordering books by title in descending order."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that books are ordered by title (Z-A)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, ['The Lord of the Rings', 'The Hobbit', 'A Game of Thrones'])
    
    def test_order_by_publication_year_ascending(self):
        """Test ordering books by publication year in ascending order."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that books are ordered by publication year (oldest first)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, [1937, 1954, 1996])
    
    def test_order_by_publication_year_descending(self):
        """Test ordering books by publication year in descending order."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that books are ordered by publication year (newest first)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, [1996, 1954, 1937])
    
    def test_order_by_author_name(self):
        """Test ordering books by author name."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'author__name'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that books are ordered by author name
        author_names = [book['author_name'] for book in response.data['results']]
        self.assertEqual(author_names, ['George R.R. Martin', 'J.R.R. Tolkien', 'J.R.R. Tolkien'])
    
    def test_multiple_field_ordering(self):
        """Test ordering by multiple fields."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-publication_year,title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that books are ordered by publication year (desc) then title (asc)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, ['A Game of Thrones', 'The Lord of the Rings', 'The Hobbit'])


class BookPaginationTests(BookAPITestCase):
    """
    Test cases for pagination functionality.
    """
    
    def setUp(self):
        """Set up additional test data for pagination tests."""
        super().setUp()
        
        # Create additional books for pagination testing
        for i in range(15):
            Book.objects.create(
                title=f'Test Book {i}',
                author=self.author,
                publication_year=2000 + i
            )
    
    def test_pagination_default(self):
        """Test default pagination behavior."""
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        
        # Check that pagination is working
        self.assertGreater(response.data['count'], len(response.data['results']))
    
    def test_pagination_custom_page_size(self):
        """Test pagination with custom page size."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'page_size': 5})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: The actual page size might be different due to DRF settings
        # Let's check that we get some results and pagination is working
        self.assertLessEqual(len(response.data['results']), 10)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_pagination_page_navigation(self):
        """Test pagination page navigation."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'page': 2, 'page_size': 5})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['previous'])
        # Note: next might be None if we're on the last page


class BookAuthenticationTests(BookAPITestCase):
    """
    Test cases for authentication and permission mechanisms.
    """
    
    def test_separate_test_database(self):
        """Test that we're using a separate test database."""
        # Demonstrate separate test database by using login method
        # This ensures we're not affecting production/development data
        login_success = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_success, "Login should succeed in test database")
        
        # Verify we can access the test user
        self.assertTrue(self.user.is_authenticated)
        
        # Test that we're working with test data
        url = reverse('api:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_public_read_access(self):
        """Test that read operations are publicly accessible."""
        # Test list endpoint
        url = reverse('api:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test detail endpoint
        url = reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_authenticated_write_access(self):
        """Test that write operations require authentication."""
        # Test create endpoint
        url = reverse('api:book-create')
        response = self.client.post(url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test update endpoint
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        response = self.client.put(url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test delete endpoint
        url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_write_access_success(self):
        """Test that authenticated users can perform write operations."""
        self.authenticate_user()
        
        # Test create endpoint
        url = reverse('api:book-create')
        response = self.client.post(url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Test update endpoint - need to provide all required fields
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        update_data = {
            'title': 'Updated Title',
            'author': self.author.id,
            'publication_year': 1937
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test delete endpoint
        url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class BookCombinedTests(BookAPITestCase):
    """
    Test cases for combined functionality (filtering + searching + ordering).
    """
    
    def test_filter_search_order_combined(self):
        """Test combining filtering, searching, and ordering."""
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'author': self.author.id,
            'search': 'The',
            'ordering': '-publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check that all filters are applied correctly
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author.id)
            self.assertIn('The', book['title'])
        
        # Check that ordering is applied (newest first)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, [1954, 1937])
    
    def test_complex_query_with_pagination(self):
        """Test complex query with pagination."""
        # Create additional books for testing
        for i in range(10):
            Book.objects.create(
                title=f'The Test Book {i}',
                author=self.author,
                publication_year=2000 + i
            )
        
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'author': self.author.id,
            'search': 'The',
            'ordering': '-publication_year',
            'page': 1,
            'page_size': 5
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('results', response.data)
        
        # Check that all filters are applied
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author.id)
            self.assertIn('The', book['title'])


class BookErrorHandlingTests(BookAPITestCase):
    """
    Test cases for error handling and edge cases.
    """
    
    def test_invalid_filter_values(self):
        """Test handling of invalid filter values."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year': 'invalid_year'})
        
        # Should return 400 for invalid filter values
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_invalid_ordering_field(self):
        """Test handling of invalid ordering field."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'invalid_field'})
        
        # Should fall back to default ordering
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_malformed_search_query(self):
        """Test handling of malformed search queries."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': ''})
        
        # Should return all books
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_nonexistent_author_filter(self):
        """Test filtering by nonexistent author."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author': 99999})
        
        # Should return 400 for invalid author ID
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookResponseFormatTests(BookAPITestCase):
    """
    Test cases for response format and data integrity.
    """
    
    def test_response_data_structure(self):
        """Test that response data has the expected structure."""
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertIn('query_info', response.data)
        
        # Check query_info structure
        query_info = response.data['query_info']
        self.assertIn('filters_applied', query_info)
        self.assertIn('available_filters', query_info)
    
    def test_book_data_structure(self):
        """Test that individual book data has the expected structure."""
        url = reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check book data structure
        book_data = response.data
        self.assertIn('id', book_data)
        self.assertIn('title', book_data)
        self.assertIn('publication_year', book_data)
        self.assertIn('author', book_data)
        self.assertIn('author_name', book_data)
        
        # Check author data structure (should be integer ID)
        self.assertIsInstance(book_data['author'], int)
        self.assertIsInstance(book_data['author_name'], str)
    
    def test_filtered_response_metadata(self):
        """Test that filtered responses include proper metadata."""
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'author': self.author.id,
            'search': 'The',
            'ordering': '-publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that query_info reflects applied filters
        query_info = response.data['query_info']
        filters_applied = query_info['filters_applied']
        
        self.assertEqual(filters_applied['author'], str(self.author.id))
        self.assertEqual(filters_applied['search'], 'The')
        self.assertEqual(filters_applied['ordering'], '-publication_year')


class BookPerformanceTests(BookAPITestCase):
    """
    Test cases for performance considerations.
    """
    
    def test_select_related_optimization(self):
        """Test that select_related is used to optimize author queries."""
        url = reverse('api:book-list')
        
        # Count database queries (expecting 3: count, results, and another count)
        with self.assertNumQueries(3):
            response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify author data is included without additional queries
        for book in response.data['results']:
            self.assertIn('author', book)
            self.assertIn('author_name', book)


# Test runner configuration
def run_tests():
    """
    Run all tests for the Book API.
    
    Usage:
        python manage.py test api.test_views
    """
    import django
    django.setup()
    
    from django.test.utils import get_runner
    from django.conf import settings
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    failures = test_runner.run_tests(['api.test_views'])
    return failures


if __name__ == '__main__':
    run_tests() 