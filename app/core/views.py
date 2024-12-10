from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.serializers import UserSerializer, UserListSerializer, UserProfileSerializer, CustomTokenObtainPairSerializer
from core.pagination import CustomPagination
from .models import User
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from core.serializers import UserAvatarSerializer
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterUserView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token_lifetime = refresh.access_token.lifetime.total_seconds()
            response_data = {
                "user": {
                    "email": user.email,
                    "name": user.name,
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "expires_in": access_token_lifetime,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserListView(generics.ListAPIView):
    """View for listing all users with pagination"""
    queryset = User.objects.all().order_by('-joined_at')
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination  # 使用自定义分页类    None  # 使用默认分页类

class UserProfileView(generics.RetrieveAPIView):
    """View for retrieving user profile"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    """View for updating user profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

class UserAvatarUpdateView(APIView):
    """View for updating user avatar"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # 允许处理文件上传

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserAvatarSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatusSerializer(serializers.Serializer):
    detail = serializers.CharField()

class FollowUserView(generics.GenericAPIView):
    """API View for following a user"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StatusSerializer  # 添加序列化器

    def post(self, request, *args, **kwargs):
        user_to_follow = get_object_or_404(User, id=self.kwargs['user_id'])
        if request.user == user_to_follow:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        if user_to_follow.followers.filter(id=request.user.id).exists():
            return Response({'detail': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        return Response({'detail': 'Successfully followed the user.'}, status=status.HTTP_201_CREATED)

class UnfollowUserView(generics.GenericAPIView):
    """API View for unfollowing a user"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StatusSerializer  # 添加序列化器

    def post(self, request, *args, **kwargs):
        user_to_unfollow = get_object_or_404(User, id=self.kwargs['user_id'])
        if not user_to_unfollow.followers.filter(id=request.user.id).exists():
            return Response({'detail': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user_to_unfollow)
        return Response({'detail': 'Successfully unfollowed the user.'}, status=status.HTTP_200_OK)


class FollowerListView(generics.ListAPIView):
    """API View for listing followers of a user"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.none()  # 默认设置为空

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        return user.followers.all()

class FollowingListView(generics.ListAPIView):
    """API View for listing users that a user is following"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.none()  # 默认设置为空

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        return user.following.all()
