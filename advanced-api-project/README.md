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

### API Endpoints
- `GET/POST /api/authors/` - List and create authors
- `GET/PUT/DELETE /api/authors/<id>/` - Retrieve, update, and delete authors
- `GET/POST /api/books/` - List and create books
- `GET/PUT/DELETE /api/books/<id>/` - Retrieve, update, and delete books
- `GET /api/test/` - Test endpoint to demonstrate serializer functionality

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

#### Create an Author
```bash
curl -X POST http://localhost:8000/api/authors/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe"}'
```

#### Create a Book
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Sample Book", "publication_year": 2020, "author": 1}'
```

#### Get Author with Books
```bash
curl http://localhost:8000/api/authors/1/
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

### Validation
- **Publication Year**: Cannot be in the future
- **Model-level Validation**: Custom clean() method in Book model
- **Serializer Validation**: Additional validation in BookSerializer

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