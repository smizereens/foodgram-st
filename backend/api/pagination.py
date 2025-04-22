from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Кастомная пагинация с указанием количества объектов на странице."""
    page_size = 6
    page_size_query_param = 'limit'