from django.contrib import admin
from django.utils.safestring import mark_safe

from recipe.models import Cart, Favorite, IngredientRecipe, Recipe, Tag


class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0

    def count_favorites(self, obj):
        return obj.favorites.count()


class CartInline(admin.TabularInline):
    model = Cart
    extra = 0


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 0
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        IngredientRecipeInline,
        FavoriteInline,
        CartInline,
    )
    list_display = (
        'id',
        'name',
        'short_image',
        'text',
        'cooking_time',
        'is_published',
        'author',
        'created_at',
        'count_favorites'
    )
    search_fields = ('name', 'author__username')
    list_filter = ('name', 'author__username', 'tags')
    empty_value_display = 'Не задано'

    def count_favorites(self, obj):
        return obj.favorites.count()

    @admin.display(description='Картинка')
    def short_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src={obj.image.url} width="80" height="60"'
            )
        return 'Нет картинки'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'recipe'
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name', 'color', 'slug',)
    ordering = ('name',)
    empty_value_display = 'Не задано'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'recipe')
    search_fields = ('author__username', 'recipe__name',)
    list_filter = ('author', 'recipe',)
    empty_value_display = 'Не задано'
