# Advanced API Project with Django REST Framework

This project demonstrates advanced API development using Django and Django REST Framework, with a focus on custom serializers that handle complex data structures and nested relationships.

## Project Overview

The project implements a book management system with Authors and Books, showcasing:
- Custom Django models with proper relationships
- Advanced serializers with nested object handling
- Data validation and error handling
- RESTful API endpoints
- Django admin interface integration

## Features

### Models
- **Author Model**: Stores author information with a one-to-many relationship to books
- **Book Model**: Stores book information with foreign key relationship to authors
- **Validation**: Publication year validation to prevent future dates
- **Relationships**: Proper foreign key relationships with related_name for reverse lookups

### Serializers
- **BookSerializer**: Handles book serialization with custom validation
- **AuthorSerializer**: Provides nested book serialization for detailed views
- **AuthorListSerializer**: Optimized for listing authors without nested data
- **Custom Validation**: Publication year validation to ensure dates are not in the future

### Views and ViewSets
- **Generic Views**: Complete CRUD operations using DRF's generic views
- **ViewSets**: Advanced ViewSets with custom actions and routing
- **Custom Actions**: Specialized endpoints for specific business logic
- **Permission Classes**: Granular access control based on user authentication and roles
- **Advanced Filtering**: Dynamic filtering, searching, and ordering capabilities

### API Endpoints

#### Basic CRUD Operations
- `GET /api/books/` - List all books (read-only)
- `GET /api/books/<id>/` - Retrieve a single book (read-only)
- `POST /api/books/create/` - Create a new book (requires authentication)
- `PUT /api/books/<id>/update/` - Update an existing book (requires authentication)
- `DELETE /api/books/<id>/delete/` - Delete a book (requires authentication)

#### Combined Endpoints
- `GET/POST /api/books/combined/` - List and create books in one endpoint
- `GET/PUT/DELETE /api/books/<id>/combined/` - Retrieve, update, and delete in one endpoint

#### Advanced Views
- `GET /api/books/advanced/` - Advanced book listing with filtering and search
- `POST /api/books/create-advanced/` - Advanced book creation with validation

#### ViewSet Endpoints (DRF Router)
- `GET/POST /api/books-viewset/` - ViewSet for books with custom actions
- `GET/PUT/DELETE /api/books-viewset/<id>/` - Individual book operations via ViewSet
- `GET /api/books-viewset/recent_books/` - Get recently published books
- `GET /api/books-viewset/book_statistics/` - Get book statistics
- `POST /api/books-viewset/<id>/duplicate_book/` - Duplicate an existing book

#### Author Endpoints
- `GET/POST /api/authors/` - List and create authors
- `GET/PUT/DELETE /api/authors/<id>/` - Retrieve, update, and delete authors
- `GET /api/authors-viewset/` - ViewSet for authors
- `GET /api/authors-viewset/<id>/books_by_author/` - Get all books by an author
- `GET /api/authors-viewset/prolific_authors/` - Get authors with most books

#### Utility Endpoints
- `GET /api/test/` - Test endpoint to demonstrate serializer functionality
- `GET /api/info/` - API information and endpoint documentation

## Installation and Setup

### Prerequisites
- Python 3.8+
- pip

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd advanced-api-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Usage

### Django Admin Interface
- Access at `http://localhost:8000/admin/`
- Use the superuser credentials to log in
- Manage authors and books through the admin interface

### API Testing
- **Test endpoint**: `http://localhost:8000/api/test/`
- **Authors API**: `http://localhost:8000/api/authors/`
- **Books API**: `http://localhost:8000/api/books/`

### Example API Usage

#### Basic CRUD Operations

**List all books:**
```bash
curl http://localhost:8000/api/books/
```

**Create a book (requires authentication):**
```bash
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"title": "Sample Book", "publication_year": 2020, "author": 1}'
```

**Update a book (requires authentication):**
```bash
curl -X PUT http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"title": "Updated Book Title", "publication_year": 2021, "author": 1}'
```

**Delete a book (requires authentication):**
```bash
curl -X DELETE http://localhost:8000/api/books/1/delete/ \
  -H "Authorization: Token YOUR_TOKEN"
```

#### Advanced Features

**Filter books by publication year:**
```bash
curl "http://localhost:8000/api/books/?min_year=2000&max_year=2020"
```

**Search books by title or author:**
```bash
curl "http://localhost:8000/api/books/advanced/?search=tolkien"
```

**Get book statistics:**
```bash
curl http://localhost:8000/api/books-viewset/book_statistics/
```

**Get recent books:**
```bash
curl http://localhost:8000/api/books-viewset/recent_books/
```

**Duplicate a book:**
```bash
curl -X POST http://localhost:8000/api/books-viewset/1/duplicate_book/ \
  -H "Authorization: Token YOUR_TOKEN"
```

#### Author Operations

**Create an author:**
```bash
curl -X POST http://localhost:8000/api/authors/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"name": "Jane Doe"}'
```

**Get author with books:**
```bash
curl http://localhost:8000/api/authors/1/
```

**Get prolific authors:**
```bash
curl http://localhost:8000/api/authors-viewset/prolific_authors/
```

## Project Structure

```
advanced-api-project/
├── advanced_api_project/     # Main project configuration
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── api/                      # API application
│   ├── __init__.py
│   ├── admin.py             # Admin interface configuration
│   ├── models.py             # Author and Book models
│   ├── serializers.py        # Custom serializers
│   ├── views.py              # API views
│   ├── urls.py               # API URL patterns
│   └── migrations/           # Database migrations
├── manage.py                 # Django management script
├── requirements.txt           # Project dependencies
└── README.md                 # This file
```

## Key Implementation Details

### Model Relationships
- **Author → Book**: One-to-many relationship using ForeignKey
- **Related Name**: `books` for reverse lookup from Author to Books
- **Cascade Delete**: Books are deleted when their author is deleted

### Serializer Features
- **Nested Serialization**: AuthorSerializer includes nested BookSerializer
- **Performance Optimization**: AuthorListSerializer excludes nested data for list views
- **Custom Validation**: Publication year validation in BookSerializer
- **Read-only Fields**: Computed fields like book_count and author_name

### View Architecture
- **Generic Views**: Standard CRUD operations with `ListAPIView`, `CreateAPIView`, etc.
- **ViewSets**: Advanced functionality with `ModelViewSet` and custom actions
- **Custom Actions**: Specialized endpoints using `@action` decorator
- **Router Integration**: Automatic URL generation for ViewSets

### Permission System
- **Granular Control**: Different permissions for different HTTP methods
- **Custom Permissions**: Advanced permission classes for complex business rules
- **Authentication Levels**: Read-only for everyone, write operations require authentication
- **Role-based Access**: Staff-only operations for sensitive actions like deletion

### Advanced Features
- **Dynamic Filtering**: Query parameter-based filtering and searching
- **Custom Querysets**: Optimized database queries with `select_related` and `prefetch_related`
- **Response Customization**: Enhanced response formatting with metadata
- **Error Handling**: Comprehensive error handling and validation

### Validation
- **Publication Year**: Cannot be in the future
- **Model-level Validation**: Custom clean() method in Book model
- **Serializer Validation**: Additional validation in BookSerializer
- **Business Logic**: Custom validation for duplicate book prevention

## Testing

### Manual Testing
1. Use the Django admin interface to create test data
2. Test API endpoints using curl or a tool like Postman
3. Verify nested serialization works correctly
4. Test validation by attempting to create books with future publication years

### Django Shell Testing
```python
python manage.py shell

from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

# Create test data
author = Author.objects.create(name="Test Author")
book = Book.objects.create(title="Test Book", author=author, publication_year=2020)

# Test serialization
serializer = AuthorSerializer(author)
print(serializer.data)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes as part of the ALX Django Learning Lab.

## Support

For questions or issues, please refer to the project documentation or create an issue in the repository. 