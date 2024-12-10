from rest_framework import serializers
from posts.models import Post, Comment, Like
from core.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts, including additional interaction information"""
    #author_name = serializers.ReadOnlyField(source='author.name')  # 保留作者名字字段
    author = UserSerializer(read_only=True)  # 嵌套用户详细信息
    like_count = serializers.IntegerField(source='likes.count', read_only=True)  # 点赞数
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)  # 评论数

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 'image', 'video',
            'tag', 'created_at', 'like_count', 'comment_count'
        ]
        read_only_fields = ['author', 'created_at', 'like_count', 'comment_count']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""
    author_name = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_name', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    """Serializer for likes"""
    user_name = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'user_name', 'created_at']
        read_only_fields = ['user', 'created_at']