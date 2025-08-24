# Social Media API - Production Deployment Guide

A comprehensive Django REST Framework-based social media API that provides user authentication, posts and comments management, user following relationships, personalized feeds, likes, and notifications system.

## 🚀 Production Deployment

### Prerequisites for Production
- Python 3.11+
- PostgreSQL 13+
- Redis (optional, for caching)
- Domain name and SSL certificate
- Cloud hosting service (Heroku, AWS, DigitalOcean, etc.)

## 📋 Deployment Checklist

### Step 1: Environment Configuration

1. **Create Production Environment Variables**
   ```bash
   cp .env.example .env
   ```

2. **Configure Production Settings**
   ```env
   SECRET_KEY=your-super-secret-production-key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_URL=postgres://user:password@host:port/dbname
   SECURE_SSL_REDIRECT=True
   SECURE_BROWSER_XSS_FILTER=True
   SECURE_CONTENT_TYPE_NOSNIFF=True
   X_FRAME_OPTIONS=DENY
   ```

### Step 2: Database Setup

1. **PostgreSQL Configuration**
   ```sql
   CREATE DATABASE social_media_api;
   CREATE USER api_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE social_media_api TO api_user;
   ```

2. **Run Migrations**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

### Step 3: Web Server Configuration

#### Option A: Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy to Heroku**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create Heroku app
   heroku create your-app-name
   
   # Add PostgreSQL addon
   heroku addons:create heroku-postgresql:mini
   
   # Set environment variables
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   
   # Deploy
   git push heroku main
   
   # Run migrations
   heroku run python manage.py migrate
   heroku run python manage.py collectstatic --noinput
   ```

3. **One-Click Heroku Deploy**
   [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

#### Option B: DigitalOcean App Platform

1. **Create app.yaml**
   ```yaml
   name: social-media-api
   services:
   - name: web
     source_dir: /
     github:
       repo: your-username/social-media-api
       branch: main
     run_command: gunicorn social_media_api.wsgi:application
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: SECRET_KEY
       value: your-secret-key
     - key: DEBUG
       value: "False"
     - key: DATABASE_URL
       value: ${db.DATABASE_URL}
   databases:
   - name: db
     engine: PG
     version: "13"
   ```

#### Option C: AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize and Deploy**
   ```bash
   eb init social-media-api
   eb create production
   eb deploy
   ```

### Step 4: Docker Deployment

1. **Build and Run with Docker**
   ```bash
   # Build the image
   docker build -t social-media-api .
   
   # Run with Docker Compose
   docker-compose up -d
   ```

2. **Production Docker Compose**
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "80:8000"
       environment:
         - DEBUG=False
         - DATABASE_URL=postgres://postgres:password@db:5432/social_media_api
       depends_on:
         - db
         - redis
     
     db:
       image: postgres:15
       environment:
         - POSTGRES_DB=social_media_api
         - POSTGRES_USER=postgres
         - POSTGRES_PASSWORD=password
       volumes:
         - postgres_data:/var/lib/postgresql/data/
     
     redis:
       image: redis:7-alpine
   
   volumes:
     postgres_data:
   ```

## 🔒 Security Configuration

### SSL/HTTPS Setup
```python
# In settings.py for production
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Additional Security Headers
```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
```

## 📊 Monitoring & Logging

### Application Monitoring
```python
# Add to settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

### Health Check Endpoint
```python
# Add to urls.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})

urlpatterns = [
    path('health/', health_check),
    # ... other patterns
]
```

## 🚀 Performance Optimization

### Database Optimization
```python
# Add database connection pooling
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

### Caching Configuration
```python
# Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## 📝 Deployment Commands

### Pre-deployment Checklist
```bash
# 1. Run tests
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
- Users can only modify their own following relationships
- Custom `IsAuthorOrReadOnly` permission class

### Feed Algorithm
- Shows posts from users the current user follows
- Ordered by creation date (newest first)
- Paginated results (10 posts per page)
- Real-time updates when following/unfollowing users

## Testing

Run the complete test suite:

```bash
# Test all apps
python manage.py test

# Test specific app
python manage.py test accounts
python manage.py test posts
```

## Social Features

### Following System
- Users can follow/unfollow other users
- View followers and following counts
- Check follow status between users
- Prevent self-following

### Personalized Feed
- Dynamic content feed based on followed users
- Chronological ordering (newest first)
- Efficient database queries
- Pagination support

## Next Steps

This foundation provides the base for extending with additional social media features such as:

- Likes and reactions on posts
- Direct messaging
- Push notifications for new posts from followed users
- Trending posts and hashtags
- Image/media uploads for posts
- User mentions and tagging
- User blocking and reporting
- Activity feeds and notifications
