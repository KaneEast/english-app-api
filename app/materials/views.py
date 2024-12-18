from rest_framework import generics
from .models import Material
from .serializers import MaterialSerializer
from core.pagination import CustomPagination  # 复用自定义分页器

class MaterialListView(generics.ListAPIView):
    """View for listing materials with category filtering and pagination"""
    serializer_class = MaterialSerializer
    pagination_class = CustomPagination  # 使用自定义分页器

    def get_queryset(self):
        queryset = Material.objects.all().order_by('-created_at')
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category)
        return queryset
