from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import CustomTokenObtainPairView

from core import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 获取 AccessToken 和 RefreshToken
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新 AccessToken
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),  # 注销 RefreshToken
    path('users/', views.UserListView.as_view(), name='user_list'),  # 用户列表
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),  # 用户更新 Profile
    path('profile/avatar/', views.UserAvatarUpdateView.as_view(), name='profile-avatar-update'),
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow-user'),
    path('followers/<int:user_id>/', views.FollowerListView.as_view(), name='follower-list'),
    path('following/<int:user_id>/', views.FollowingListView.as_view(), name='following-list'),
]
