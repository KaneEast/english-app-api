from rest_framework import serializers
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return User.objects.create_user(**validated_data)

class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users"""

    class Meta:
        model = User
        fields = ['id', 'name', 'bio', 'avatar', 'joined_at']

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""

    class Meta:
        model = User
        fields = ['name', 'bio', 'avatar']
        extra_kwargs = {
            'avatar': {'required': False},
        }
