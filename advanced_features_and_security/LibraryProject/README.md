# LibraryProject – Django Setup
This project was created as part of the ALX Django learning module.

## Security Best Practices

- DEBUG is set to False for production.
- SECURE_BROWSER_XSS_FILTER, X_FRAME_OPTIONS, and SECURE_CONTENT_TYPE_NOSNIFF are enabled for browser-side protections.
- CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE are set to True to ensure cookies are sent over HTTPS only.
- All forms include {% csrf_token %} for CSRF protection.
- Django ORM is used for all database access to prevent SQL injection.
- django-csp is used to set a Content Security Policy (CSP) header to mitigate XSS attacks.
- See settings.py for detailed security configuration and comments.

## HTTPS and Secure Redirects

- SECURE_SSL_REDIRECT is enabled to force all HTTP requests to HTTPS.
- SECURE_HSTS_SECONDS, SECURE_HSTS_INCLUDE_SUBDOMAINS, and SECURE_HSTS_PRELOAD are set to enforce HSTS and allow browser preload.
- SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE ensure cookies are only sent over HTTPS.
- X_FRAME_OPTIONS, SECURE_CONTENT_TYPE_NOSNIFF, and SECURE_BROWSER_XSS_FILTER are set for additional browser-side security.

### Deployment Configuration
- To serve your Django app over HTTPS, configure your web server (e.g., Nginx or Apache) with a valid SSL/TLS certificate.
- Example (Nginx):

```
server {
    listen 443 ssl;
    server_name yourdomain.com;
    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;
    ...
    location / {
        proxy_pass http://127.0.0.1:8000;
        ...
    }
}
```

### Security Review
- All recommended Django security settings for HTTPS and secure cookies are enabled.
- HSTS is enforced for one year and includes subdomains.
- All cookies are secure and only sent over HTTPS.
- HTTP requests are redirected to HTTPS.
- Additional browser-side protections are enabled.
- For further improvement, consider using automated security scanning tools and regular reviews.
