from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    
    This permission class checks if the user is the owner of the object
    before allowing write operations. Read operations are always allowed.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object.
        
        Args:
            request: The request object
            view: The view being accessed
            obj: The object being accessed
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        # For now, we'll allow any authenticated user to edit
        # You can extend this to check actual ownership
        return request.user.is_authenticated


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to perform write operations.
    
    This permission class restricts write operations to admin users only,
    while allowing read access to everyone.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.
        
        Args:
            request: The request object
            view: The view being accessed
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admin users
        return request.user.is_authenticated and request.user.is_staff


class IsAuthenticatedOrReadOnlyForBooks(permissions.BasePermission):
    """
    Custom permission for books that allows read access to everyone
    but requires authentication for write operations.
    
    This permission class is specifically designed for book operations
    and can be extended with additional business logic.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.
        
        Args:
            request: The request object
            view: The view being accessed
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions require authentication
        if not request.user.is_authenticated:
            return False
        
        # Additional checks can be added here
        # For example, checking if user has verified email
        # or if user account is active
        
        return True
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the specific object.
        
        Args:
            request: The request object
            view: The view being accessed
            obj: The object being accessed
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions require authentication
        if not request.user.is_authenticated:
            return False
        
        # Additional object-level checks can be added here
        # For example, checking if user is the creator of the book
        # or if user has special permissions
        
        return True


class BookActionPermission(permissions.BasePermission):
    """
    Advanced permission class for book actions with different rules
    for different operations.
    
    This permission class demonstrates how to implement complex
    permission logic based on the specific action being performed.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.
        
        Args:
            request: The request object
            view: The view being accessed
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        # Always allow read operations
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check the specific action being performed
        action = getattr(view, 'action', None)
        
        if action == 'create':
            # Creating books requires authentication
            return request.user.is_authenticated
        
        elif action == 'update':
            # Updating books requires authentication
            return request.user.is_authenticated
        
        elif action == 'partial_update':
            # Partial updates require authentication
            return request.user.is_authenticated
        
        elif action == 'destroy':
            # Deleting books requires authentication and staff status
            return request.user.is_authenticated and request.user.is_staff
        
        # Default to requiring authentication for any other write operations
        return request.user.is_authenticated 