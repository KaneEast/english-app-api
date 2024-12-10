from django.urls import path
from posts import views

urlpatterns = [
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('list/', views.PostListView.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),  # 删除动态

    path('comments/create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:post_id>/', views.CommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),  # 删除评论

    path('likes/create/', views.LikeCreateView.as_view(), name='like-create'),
    path('likes/<int:post_id>/delete/', views.LikeDeleteView.as_view(), name='like-delete'),

]
