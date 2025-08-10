# Filtering, Searching, and Ordering in Django REST Framework API

This document provides comprehensive documentation for the advanced filtering, searching, and ordering capabilities implemented in the Book Management API.

## Overview

The API provides sophisticated query capabilities that allow users to:
- **Filter** books by various attributes using exact matches and ranges
- **Search** across book titles and author names with case-insensitive matching
- **Order** results by any field in ascending or descending order
- **Combine** multiple filters for precise data retrieval

## Available Endpoints

### 1. Book List View (`/api/books/`)
- **Method**: GET
- **Permissions**: Public access (AllowAny)
- **Features**: Full filtering, searching, and ordering capabilities

### 2. Book List-Create View (`/api/books/combined/`)
- **Method**: GET, POST
- **Permissions**: Read (AllowAny), Write (IsAuthenticated)
- **Features**: Same filtering capabilities as Book List View

### 3. Advanced Book List View (`/api/books/advanced/`)
- **Method**: GET
- **Permissions**: Public access (AllowAny)
- **Features**: Advanced custom filtering with enhanced response metadata

## Filtering Capabilities

### Exact Match Filters

These filters perform exact matching on specific fields:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `author` | Integer | Filter by author ID | `?author=1` |
| `publication_year` | Integer | Filter by exact publication year | `?publication_year=2020` |

### Range Filters

These filters allow filtering within a range:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `year_from` | Integer | Books published from this year onwards | `?year_from=2015` |
| `year_to` | Integer | Books published up to this year | `?year_to=2023` |

### Custom Filters

These filters provide specialized matching capabilities:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `title_starts_with` | String | Books whose title starts with the given string | `?title_starts_with=Harry` |
| `author_contains` | String | Books by authors whose name contains the string | `?author_contains=Rowling` |

## Search Functionality

### Search Parameters

The API provides case-insensitive search across multiple fields:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search` | String | Search in book title and author name | `?search=python` |

### Search Fields

The search functionality covers:
- **Book Title**: Searches within the book title
- **Author Name**: Searches within the author's name

### Search Behavior

- **Case-insensitive**: Searches are not case-sensitive
- **Partial matching**: Matches any part of the text
- **Multiple fields**: Searches across both title and author name simultaneously

## Ordering Capabilities

### Ordering Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `ordering` | String | Order results by field(s) | `?ordering=title` |

### Available Ordering Fields

| Field | Description | Ascending | Descending |
|-------|-------------|-----------|------------|
| `title` | Book title | `?ordering=title` | `?ordering=-title` |
| `publication_year` | Publication year | `?ordering=publication_year` | `?ordering=-publication_year` |
| `author__name` | Author name | `?ordering=author__name` | `?ordering=-author__name` |
| `id` | Book ID | `?ordering=id` | `?ordering=-id` |

### Multiple Field Ordering

You can order by multiple fields by separating them with commas:

```
?ordering=-publication_year,title
```

This orders by publication year (descending) first, then by title (ascending).

### Default Ordering

If no ordering is specified, the API defaults to:
```
-ordering=-publication_year,title
```

## Pagination

The API supports pagination for large result sets:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `page` | Integer | Page number (1-based) | `?page=2` |
| `page_size` | Integer | Number of items per page | `?page_size=10` |

## Usage Examples

### Basic Filtering

```bash
# Filter by author
GET /api/books/?author=1

# Filter by publication year
GET /api/books/?publication_year=2020

# Filter by year range
GET /api/books/?year_from=2015&year_to=2023
```

### Search Examples

```bash
# Search for books containing "python"
GET /api/books/?search=python

# Search for books by author containing "Rowling"
GET /api/books/?search=rowling
```

### Ordering Examples

```bash
# Order by title (ascending)
GET /api/books/?ordering=title

# Order by publication year (descending)
GET /api/books/?ordering=-publication_year

# Multiple field ordering
GET /api/books/?ordering=-publication_year,title
```

### Combined Queries

```bash
# Search and filter
GET /api/books/?search=python&year_from=2015&year_to=2023

# Filter, search, and order
GET /api/books/?author=1&search=programming&ordering=-publication_year

# Complex query with pagination
GET /api/books/?search=harry&year_from=2000&ordering=title&page=2&page_size=10
```

### Custom Filters

```bash
# Books whose title starts with "Harry"
GET /api/books/?title_starts_with=Harry

# Books by authors whose name contains "King"
GET /api/books/?author_contains=King

# Combine custom filters
GET /api/books/?title_starts_with=The&author_contains=Stephen&year_from=1980
```

## Response Format

### Standard Response

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/books/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Python Programming",
      "publication_year": 2020,
      "author": {
        "id": 1,
        "name": "John Doe"
      }
    }
  ]
}
```

### Enhanced Response (with query metadata)

```json
{
  "message": "Books retrieved successfully",
  "total_count": 25,
  "books": [...],
  "query_info": {
    "filters_applied": {
      "author": "1",
      "publication_year": null,
      "year_from": "2015",
      "year_to": "2023",
      "search": "python",
      "title_starts_with": null,
      "author_contains": null,
      "ordering": "-publication_year,title"
    },
    "available_filters": {
      "exact_match": ["author", "publication_year"],
      "range_filters": ["year_from", "year_to"],
      "search_fields": ["title", "author__name"],
      "ordering_fields": ["title", "publication_year", "author__name", "id"],
      "custom_filters": ["title_starts_with", "author_contains"]
    }
  }
}
```

## Implementation Details

### Filter Backends Used

1. **DjangoFilterBackend**: Provides exact match filtering
2. **SearchFilter**: Enables text search across specified fields
3. **OrderingFilter**: Handles result ordering

### Custom Filtering Logic

The API implements custom filtering logic in the `get_queryset()` method to provide:
- Range filtering for publication years
- Prefix matching for book titles
- Contains matching for author names

### Performance Optimizations

- **select_related()**: Optimizes database queries for author information
- **Database indexes**: Ensures efficient filtering and searching
- **Query optimization**: Minimizes database hits

## Error Handling

The API gracefully handles invalid parameters:
- Invalid filter values return empty results
- Invalid ordering fields fall back to default ordering
- Malformed search queries are handled safely

## Testing

### Manual Testing

You can test the API using:
- **Postman**: Import the collection and test various queries
- **curl**: Use command-line requests
- **Browser**: Direct URL testing for GET requests

### Example curl Commands

```bash
# Basic filtering
curl "http://localhost:8000/api/books/?author=1"

# Search and order
curl "http://localhost:8000/api/books/?search=python&ordering=-publication_year"

# Complex query
curl "http://localhost:8000/api/books/?year_from=2015&year_to=2023&search=programming&ordering=title&page=1&page_size=5"
```

## Best Practices

1. **Use specific filters** when you know exact values
2. **Combine filters** for more precise results
3. **Use search** for text-based queries
4. **Apply ordering** to get consistent results
5. **Use pagination** for large datasets
6. **Cache results** when appropriate for performance

## Future Enhancements

Potential improvements for the filtering system:
- Full-text search with relevance scoring
- Faceted search capabilities
- Advanced date range filtering
- Fuzzy matching for search queries
- Custom filter backends for complex queries 