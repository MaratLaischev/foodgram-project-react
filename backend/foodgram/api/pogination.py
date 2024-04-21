from rest_framework.pagination import PageNumberPagination

from foodgram.settings import DEFAULT_PAGE_SIZE_POGINATION


class RecipePogination(PageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE_POGINATION
    page_size_query_param = 'limit'
