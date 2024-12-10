from rest_framework import serializers
#from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import User
from datetime import timedelta
from django.conf import settings
from django.utils.timezone import now

# class UserSerializer(serializers.ModelSerializer):
#     """Serializer for the user object"""

#     class Meta:
#         model = User
#         password = serializers.CharField(
#             max_length=68, min_length=6, write_only=True)

#         fields = ['id', 'email', 'name', 'password', 'avatar', 'bio', 'joined_at']
#         # extra_kwargs = {
#         #     #'password': {'write_only': True, 'min_length': 5}
#         #     'password': {'min_length': 5}
#         # }

#     def create(self, validated_data):
#         """Create and return a user with encrypted password"""
#         return User.objects.create_user(**validated_data)
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = User
        fields = ['id', 'name', 'avatar', 'bio', 'joined_at']  # 移除 email 和 password
        read_only_fields = ['id', 'joined_at']

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
        fields = ['name', 'bio']
        extra_kwargs = {
            'bio': {'required': False},
        }

class UserAvatarSerializer(serializers.ModelSerializer):
    """Serializer for updating user avatar"""

    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['avatar', 'avatar_url']
        extra_kwargs = {
            'avatar': {'required': True},
        }

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            # 添加时间戳强制刷新缓存
            timestamp = int(now().timestamp())
            return f"{request.build_absolute_uri(obj.avatar.url)}?v={timestamp}"
        return None

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # 添加额外信息
        data['token_type'] = 'Bearer'
        # 使用 total_seconds() 获取整个生命周期的秒数
        data['expires_in'] = int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())

        return data