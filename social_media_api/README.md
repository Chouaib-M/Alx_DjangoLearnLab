# Social Media API

A Django REST Framework-based social media API with user authentication, profile management, and social features.

## Features

- **User Authentication**: Registration, login, and token-based authentication
- **Custom User Model**: Extended user model with bio, profile picture, and followers
- **Profile Management**: View and update user profiles
- **Social Features**: Follow/unfollow users, view followers and following
- **User Discovery**: List and search users

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

### Get User Profile

```bash
curl -X GET http://127.0.0.1:8000/api/accounts/profile/ \
  -H "Authorization: Token your_token_here"
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
└── accounts/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── tests.py
```

## Security Features

- Password validation using Django's built-in validators
- CSRF protection for web forms
- Token-based authentication for API endpoints
- User permission checks for profile modifications
- Secure file upload handling for profile pictures

## Next Steps

This foundation provides the base for extending with additional social media features such as:

- Posts and content creation
- Comments and likes
- Direct messaging
- Notifications
- Content feeds
- Search functionality
