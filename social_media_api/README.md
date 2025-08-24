# Social Media API

A Django REST Framework-based social media API with user authentication, profile management, posts, comments, and social features.

## Features

- **User Authentication**: Registration, login, and token-based authentication
- **Custom User Model**: Extended user model with bio, profile picture, and followers
- **Profile Management**: View and update user profiles
- **Social Features**: Follow/unfollow users, view followers and following
- **User Discovery**: List and search users
- **Posts Management**: Create, read, update, delete posts with pagination and filtering
- **Comments System**: Add, edit, delete comments on posts
- **Advanced Filtering**: Search posts by title/content, filter by author and date
- **Permissions**: Users can only edit/delete their own posts and comments

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

4. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication

- **POST** `/api/accounts/register/` - Register a new user
- **POST** `/api/accounts/login/` - Login user

### Profile Management

- **GET** `/api/accounts/profile/` - Get current user profile
- **PUT/PATCH** `/api/accounts/profile/` - Update current user profile

### User Discovery

- **GET** `/api/accounts/users/` - List all users
- **GET** `/api/accounts/users/{id}/` - Get specific user profile

### Social Features

- **POST** `/api/accounts/follow/{user_id}/` - Follow/unfollow a user

### Posts Management

- **GET** `/api/posts/` - List all posts (with pagination, filtering, search)
- **POST** `/api/posts/` - Create a new post
- **GET** `/api/posts/{id}/` - Get specific post with comments
- **PUT/PATCH** `/api/posts/{id}/` - Update own post
- **DELETE** `/api/posts/{id}/` - Delete own post
- **GET** `/api/posts/{id}/comments/` - Get all comments for a post
- **POST** `/api/posts/{id}/add_comment/` - Add comment to a post

### Comments Management

- **GET** `/api/comments/` - List all comments (with pagination and filtering)
- **POST** `/api/comments/` - Create a new comment
- **GET** `/api/comments/{id}/` - Get specific comment
- **PUT/PATCH** `/api/comments/{id}/` - Update own comment
- **DELETE** `/api/comments/{id}/` - Delete own comment

## User Model

The custom user model extends Django's `AbstractUser` with additional fields:

- `bio`: Text field for user biography (max 500 characters)
- `profile_picture`: Image field for profile picture
- `followers`: Many-to-many relationship for follower functionality

## Authentication

The API uses Django REST Framework's token authentication. Include the token in the Authorization header:

```
Authorization: Token your_token_here
```

## Usage Examples

### Register a New User

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Hello, I am John!"
  }'
```

### Login User

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

### Create a Post

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post!"
  }'
```

### Get Posts with Filtering

```bash
# Get all posts
curl -X GET http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token your_token_here"

# Search posts by title/content
curl -X GET "http://127.0.0.1:8000/api/posts/?search=first" \
  -H "Authorization: Token your_token_here"

# Filter posts by author
curl -X GET "http://127.0.0.1:8000/api/posts/?author=1" \
  -H "Authorization: Token your_token_here"
```

### Add Comment to Post

```bash
curl -X POST http://127.0.0.1:8000/api/posts/1/add_comment/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Great post! Thanks for sharing."
  }'
```

### Follow a User

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/follow/2/ \
  -H "Authorization: Token your_token_here"
```

## Testing

Run the test suite:

```bash
python manage.py test accounts
```

## Project Structure

```
social_media_api/
├── manage.py
├── requirements.txt
├── README.md
├── social_media_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
└── posts/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── permissions.py
    ├── urls.py
    └── tests.py
```

## Security Features

- Password validation using Django's built-in validators
- CSRF protection for web forms
- Token-based authentication for API endpoints
- User permission checks for profile modifications
- Secure file upload handling for profile pictures

## Advanced Features

### Pagination
All list endpoints support pagination with configurable page size (default: 10 items per page).

### Filtering and Search
- **Posts**: Filter by author, creation date; search by title and content
- **Comments**: Filter by author, post, creation date; search by content
- **Ordering**: Sort by creation date, update date, and other relevant fields

### Permissions
- Users can only edit/delete their own posts and comments
- All authenticated users can view posts and comments
- Custom `IsAuthorOrReadOnly` permission class

## Testing

Run the complete test suite:

```bash
# Test all apps
python manage.py test

# Test specific app
python manage.py test accounts
python manage.py test posts
```

## Next Steps

This foundation provides the base for extending with additional social media features such as:

- Likes and reactions on posts
- Direct messaging
- Notifications
- Content feeds and timelines
- Image/media uploads for posts
- Hashtags and mentions
- User blocking and reporting
