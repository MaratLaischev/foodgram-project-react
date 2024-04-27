from django.contrib import admin

from ingredient.models import Ingredient
from recipe.models import IngredientRecipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name',)
    list_filter = ('recipe', 'ingredient',)
    empty_value_display = 'не задано'
