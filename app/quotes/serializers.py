from rest_framework import serializers
from .models import Quote, Celebrity

class CelebritySerializer(serializers.ModelSerializer):
    """Serializer for Celebrity model with quote count"""
    quote_count = serializers.SerializerMethodField()

    class Meta:
        model = Celebrity
        fields = ['id', 'name', 'title', 'quote_count']  # 添加 quote_count 字段

    def get_quote_count(self, obj):
        return obj.quotes.count()  # 返回关联的 Quote 数量

class QuoteSerializer(serializers.ModelSerializer):
    """Serializer for the Quote model with nested Celebrity information"""
    celebrity = CelebritySerializer(read_only=True)  # 嵌套序列化器

    class Meta:
        model = Quote
        fields = ['id', 'content', 'tag', 'celebrity']  # 包括嵌套的 celebrity 字段
