from rest_framework.pagination import PageNumberPagination

from foodgram.constants import DEFAULT_PAGE_SIZE_PAGINATOR


class RecipePaginator(PageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE_PAGINATOR
    page_size_query_param = 'limit'
