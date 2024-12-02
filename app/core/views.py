from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.serializers import UserSerializer, UserListSerializer, UserProfileSerializer
from core.pagination import CustomPagination
from .models import User

class RegisterUserView(APIView):
    """Create a new user in the system"""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    """View for listing all users with pagination"""
    queryset = User.objects.all().order_by('-joined_at')
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination  # 使用自定义分页类    None  # 使用默认分页类

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    """View for updating user profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user