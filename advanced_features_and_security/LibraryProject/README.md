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
