from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from posts.models import Comment, Like, Post
from posts.serializers import PostSerializer, CommentSerializer, LikeSerializer
from posts.pagination import PostPagination
from core.pagination import CustomPagination

class PostCreateView(generics.CreateAPIView):
    """View for creating a new post"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Set the author to the logged-in user"""
        serializer.save(author=self.request.user)

class PostListView(generics.ListAPIView):
    """View for listing all posts with custom pagination and additional information"""
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    pagination_class = CustomPagination#PostPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['author', 'tag']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class PostUpdateView(generics.UpdateAPIView):
    """View for updating a specific post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionError('You do not have permission to edit this post.')
        serializer.save()

class PostDeleteView(generics.DestroyAPIView):
    """View for deleting a specific post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionError('You do not have permission to delete this post.')
        instance.delete()

class PostDetailView(generics.RetrieveAPIView):
    """View for retrieving a specific post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

class CommentCreateView(generics.CreateAPIView):
    """View for creating a new comment"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = generics.get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

class CommentListView(generics.ListAPIView):
    """View for listing comments on a post"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Comment.objects.none()  # 默认设置为空，防止生成文档时出现问题

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        if post_id is not None:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.none()

class CommentUpdateView(generics.UpdateAPIView):
    """View for updating a specific comment"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionError('You do not have permission to edit this comment.')
        serializer.save()

class CommentDeleteView(generics.DestroyAPIView):
    """View for deleting a specific comment"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionError('You do not have permission to delete this comment.')
        instance.delete()

class LikeCreateView(generics.CreateAPIView):
    """View for liking a post"""
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = generics.get_object_or_404(Post, id=post_id)
        if Like.objects.filter(post=post, user=self.request.user).exists():
            raise ValidationError('You have already liked this post')
        serializer.save(user=self.request.user, post=post)

class LikeDeleteView(generics.DestroyAPIView):
    """View for unliking a post"""
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        post_id = self.kwargs['post_id']
        user = self.request.user
        like = Like.objects.filter(post_id=post_id, user=user).first()
        if not like:
            raise ValidationError('You have not liked this post')
        return like
