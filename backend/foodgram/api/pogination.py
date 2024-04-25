from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class RecipePogination(PageNumberPagination):
    page_size = settings.DEFAULT_PAGE_SIZE_POGINATION
    page_size_query_param = 'limit'
