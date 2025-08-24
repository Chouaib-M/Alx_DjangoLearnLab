from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles user creation with password validation and confirmation.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'bio')

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def create(self, validated_data):
        """Create and return a new user instance."""
        validated_data.pop('password_confirm')
        user = get_user_model().objects.create_user(**validated_data)
        # Create token for the new user
        Token.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates username/password and returns user if authentication succeeds.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Authenticate user with provided credentials."""
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include username and password.')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    Includes read-only fields for followers and following counts.
    """
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    followers = serializers.StringRelatedField(many=True, read_only=True)
    following = serializers.StringRelatedField(many=True, read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'bio', 'profile_picture', 'followers_count', 'following_count',
            'followers', 'following', 'is_following', 'date_joined'
        )
        read_only_fields = ('id', 'username', 'date_joined')
    
    def get_is_following(self, obj):
        """Check if the current user is following this user."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile information.
    Allows updating of specific fields only.
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'bio', 'profile_picture')

    def validate_email(self, value):
        """Ensure email is unique."""
        user = self.instance
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
