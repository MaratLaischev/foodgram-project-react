from rest_framework.pagination import PageNumberPagination

from foodgram.constants import DEFAULT_PAGE_SIZE_POGINATOR


class RecipePaginator(PageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE_POGINATOR
    page_size_query_param = 'limit'
