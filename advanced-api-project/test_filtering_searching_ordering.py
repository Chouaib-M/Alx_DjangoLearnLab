#!/usr/bin/env python3
"""
Test Script for Filtering, Searching, and Ordering Capabilities

This script demonstrates and tests the advanced filtering, searching, and ordering
features implemented in the Django REST Framework API.

Usage:
    python test_filtering_searching_ordering.py

Requirements:
    - Django server running on localhost:8000
    - Some test data in the database
"""

import requests
import json
from urllib.parse import urlencode

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def print_separator(title):
    """Print a formatted separator with title."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def make_request(endpoint, params=None):
    """Make a GET request to the API and return the response."""
    url = f"{BASE_URL}{endpoint}"
    if params:
        url += "?" + urlencode(params)
    
    print(f"Request: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def print_response(data, title="Response"):
    """Print formatted response data."""
    print(f"\n{title}:")
    print("-" * 40)
    
    if isinstance(data, dict):
        if 'results' in data:
            # Paginated response
            print(f"Total Count: {data.get('count', 'N/A')}")
            print(f"Next Page: {data.get('next', 'None')}")
            print(f"Previous Page: {data.get('previous', 'None')}")
            print(f"Results: {len(data['results'])} items")
            
            for i, item in enumerate(data['results'], 1):
                print(f"  {i}. {item.get('title', 'N/A')} by {item.get('author', {}).get('name', 'N/A')} ({item.get('publication_year', 'N/A')})")
        else:
            # Custom response format
            print(json.dumps(data, indent=2))
    else:
        print(data)

def test_basic_filtering():
    """Test basic filtering capabilities."""
    print_separator("BASIC FILTERING TESTS")
    
    # Test 1: Filter by author
    print("\n1. Filter by author ID:")
    data = make_request("/books/", {"author": 1})
    print_response(data, "Books by Author ID 1")
    
    # Test 2: Filter by publication year
    print("\n2. Filter by publication year:")
    data = make_request("/books/", {"publication_year": 2020})
    print_response(data, "Books published in 2020")
    
    # Test 3: Filter by year range
    print("\n3. Filter by year range:")
    data = make_request("/books/", {"year_from": 2015, "year_to": 2023})
    print_response(data, "Books published between 2015-2023")

def test_search_functionality():
    """Test search functionality."""
    print_separator("SEARCH FUNCTIONALITY TESTS")
    
    # Test 1: Search in titles and author names
    print("\n1. Search for 'python':")
    data = make_request("/books/", {"search": "python"})
    print_response(data, "Search results for 'python'")
    
    # Test 2: Search for author name
    print("\n2. Search for author name:")
    data = make_request("/books/", {"search": "rowling"})
    print_response(data, "Search results for 'rowling'")
    
    # Test 3: Search with no results
    print("\n3. Search with no results:")
    data = make_request("/books/", {"search": "nonexistentbook"})
    print_response(data, "Search results for 'nonexistentbook'")

def test_ordering_capabilities():
    """Test ordering capabilities."""
    print_separator("ORDERING CAPABILITIES TESTS")
    
    # Test 1: Order by title (ascending)
    print("\n1. Order by title (ascending):")
    data = make_request("/books/", {"ordering": "title"})
    print_response(data, "Books ordered by title (A-Z)")
    
    # Test 2: Order by title (descending)
    print("\n2. Order by title (descending):")
    data = make_request("/books/", {"ordering": "-title"})
    print_response(data, "Books ordered by title (Z-A)")
    
    # Test 3: Order by publication year (descending)
    print("\n3. Order by publication year (descending):")
    data = make_request("/books/", {"ordering": "-publication_year"})
    print_response(data, "Books ordered by publication year (newest first)")
    
    # Test 4: Multiple field ordering
    print("\n4. Multiple field ordering:")
    data = make_request("/books/", {"ordering": "-publication_year,title"})
    print_response(data, "Books ordered by publication year (desc) then title (asc)")

def test_custom_filters():
    """Test custom filtering capabilities."""
    print_separator("CUSTOM FILTERS TESTS")
    
    # Test 1: Title starts with
    print("\n1. Books whose title starts with 'The':")
    data = make_request("/books/", {"title_starts_with": "The"})
    print_response(data, "Books with title starting with 'The'")
    
    # Test 2: Author name contains
    print("\n2. Books by authors whose name contains 'King':")
    data = make_request("/books/", {"author_contains": "King"})
    print_response(data, "Books by authors with 'King' in name")
    
    # Test 3: Combine custom filters
    print("\n3. Combine custom filters:")
    data = make_request("/books/", {
        "title_starts_with": "The",
        "author_contains": "Stephen",
        "year_from": 1980
    })
    print_response(data, "Books with title starting 'The', author containing 'Stephen', published after 1980")

def test_combined_queries():
    """Test combined filtering, searching, and ordering."""
    print_separator("COMBINED QUERIES TESTS")
    
    # Test 1: Search + Filter + Order
    print("\n1. Search + Filter + Order:")
    data = make_request("/books/", {
        "search": "programming",
        "year_from": 2015,
        "ordering": "-publication_year"
    })
    print_response(data, "Programming books from 2015 onwards, newest first")
    
    # Test 2: Complex query with pagination
    print("\n2. Complex query with pagination:")
    data = make_request("/books/", {
        "search": "harry",
        "year_from": 2000,
        "ordering": "title",
        "page": 1,
        "page_size": 5
    })
    print_response(data, "Harry books from 2000 onwards, ordered by title, page 1")

def test_different_endpoints():
    """Test filtering on different endpoints."""
    print_separator("DIFFERENT ENDPOINTS TESTS")
    
    # Test 1: Book List View
    print("\n1. Book List View (/books/):")
    data = make_request("/books/", {"search": "python", "ordering": "title"})
    print_response(data, "Book List View Results")
    
    # Test 2: Book List-Create View
    print("\n2. Book List-Create View (/books/combined/):")
    data = make_request("/books/combined/", {"search": "python", "ordering": "title"})
    print_response(data, "Book List-Create View Results")
    
    # Test 3: Advanced Book List View
    print("\n3. Advanced Book List View (/books/advanced/):")
    data = make_request("/books/advanced/", {"search": "python", "ordering": "title"})
    print_response(data, "Advanced Book List View Results")

def test_error_handling():
    """Test error handling for invalid parameters."""
    print_separator("ERROR HANDLING TESTS")
    
    # Test 1: Invalid author ID
    print("\n1. Invalid author ID:")
    data = make_request("/books/", {"author": 99999})
    print_response(data, "Invalid author ID")
    
    # Test 2: Invalid publication year
    print("\n2. Invalid publication year:")
    data = make_request("/books/", {"publication_year": 9999})
    print_response(data, "Invalid publication year")
    
    # Test 3: Invalid ordering field
    print("\n3. Invalid ordering field:")
    data = make_request("/books/", {"ordering": "invalid_field"})
    print_response(data, "Invalid ordering field")

def test_response_metadata():
    """Test response metadata and query information."""
    print_separator("RESPONSE METADATA TESTS")
    
    # Test enhanced response with query metadata
    print("\n1. Enhanced response with query metadata:")
    data = make_request("/books/", {
        "author": 1,
        "year_from": 2015,
        "search": "python",
        "ordering": "-publication_year"
    })
    
    if data and 'query_info' in data:
        print("\nQuery Information:")
        print(f"  Filters Applied: {data['query_info']['filters_applied']}")
        print(f"  Available Filters: {data['query_info']['available_filters']}")
        print(f"  Total Count: {data.get('total_count', 'N/A')}")
    else:
        print_response(data, "Response with metadata")

def main():
    """Main function to run all tests."""
    print("Django REST Framework API - Filtering, Searching, and Ordering Tests")
    print("=" * 70)
    
    try:
        # Test basic functionality
        test_basic_filtering()
        test_search_functionality()
        test_ordering_capabilities()
        test_custom_filters()
        test_combined_queries()
        test_different_endpoints()
        test_error_handling()
        test_response_metadata()
        
        print_separator("TESTING COMPLETE")
        print("All tests completed successfully!")
        print("\nTo test manually, you can use the following curl commands:")
        print("\n# Basic filtering:")
        print("curl 'http://localhost:8000/api/books/?author=1'")
        print("\n# Search and order:")
        print("curl 'http://localhost:8000/api/books/?search=python&ordering=-publication_year'")
        print("\n# Complex query:")
        print("curl 'http://localhost:8000/api/books/?year_from=2015&year_to=2023&search=programming&ordering=title&page=1&page_size=5'")
        
    except KeyboardInterrupt:
        print("\n\nTesting interrupted by user.")
    except Exception as e:
        print(f"\nError during testing: {e}")

if __name__ == "__main__":
    main() 