from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserUpdateSerializer
)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """
    Register a new user and return authentication token.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'User registered successfully',
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    """
    Authenticate user and return authentication token.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update user profile.
    Users can only access and modify their own profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserUpdateSerializer
        return UserProfileSerializer


class UserListView(generics.ListAPIView):
    """
    List all users (for discovery purposes).
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveAPIView):
    """
    Retrieve specific user profile by ID.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user.
    """
    try:
        user_to_follow = CustomUser.objects.get(id=user_id)
        current_user = request.user
        
        if current_user == user_to_follow:
            return Response({
                'error': 'You cannot follow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if current_user.is_following(user_to_follow):
            return Response({
                'error': 'You are already following this user'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        current_user.follow(user_to_follow)
        
        return Response({
            'message': f'You are now following {user_to_follow.username}',
            'following': True,
            'followers_count': user_to_follow.followers_count
        }, status=status.HTTP_200_OK)
        
    except CustomUser.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user.
    """
    try:
        user_to_unfollow = CustomUser.objects.get(id=user_id)
        current_user = request.user
        
        if current_user == user_to_unfollow:
            return Response({
                'error': 'You cannot unfollow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not current_user.is_following(user_to_unfollow):
            return Response({
                'error': 'You are not following this user'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        current_user.unfollow(user_to_unfollow)
        
        return Response({
            'message': f'You unfollowed {user_to_unfollow.username}',
            'following': False,
            'followers_count': user_to_unfollow.followers_count
        }, status=status.HTTP_200_OK)
        
    except CustomUser.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
