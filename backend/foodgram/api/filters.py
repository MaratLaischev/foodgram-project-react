import django_filters

from ingredient.models import Ingredient
from recipe.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    is_favorited = django_filters.BooleanFilter(method='get_favorite')
    is_in_shopping_cart = django_filters.BooleanFilter(method='get_cart')
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']

    def get_favorite(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__author=user)
        return queryset

    def get_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(carts__author=user)
        return queryset


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')
