from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from core import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 获取 AccessToken 和 RefreshToken
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新 AccessToken
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),  # 注销 RefreshToken
    path('users/', views.UserListView.as_view(), name='user_list'),  # 用户列表
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),  # 用户更新 Profile
]
