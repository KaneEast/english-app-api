from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 20  # 每页显示 5 条动态
    page_size_query_param = 'page_size'
    max_page_size = 20
