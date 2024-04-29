from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from random import randint

from foodgram import constants
from ingredient.models import Ingredient
from user.models import User


def default_color():
    color_1 = format(randint(16, 255), 'X')
    color_2 = format(randint(16, 255), 'X')
    color_3 = format(randint(16, 255), 'X')
    return f'#{color_1}{color_2}{color_3}'


class Tag(models.Model):
    name = models.CharField(
        'Название', max_length=constants.MAX_LENGTH, unique=True
    )
    color = ColorField(
        'Цвет', default=default_color,
        unique=True, max_length=constants.MAX_LENGTH_COLOR
    )
    slug = models.SlugField(
        'Уникальный слаг', max_length=constants.MAX_LENGTH, unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:constants.RESTRICTION_STRING]


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор',
    )
    name = models.CharField('Название', max_length=constants.MAX_LENGTH)
    image = models.ImageField('Картинка', upload_to='recipe_img/', blank=True)
    text = models.TextField('Описание')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    ingredients = models.ManyToManyField(
        'IngredientRecipe', verbose_name='Ингредиенты'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в мин.',
        validators=(MinValueValidator(
            constants.MINIMUM_COOKING_TIME,
            message=(
                'Минимальное время приготовления'
                f'{constants.MINIMUM_COOKING_TIME} минута'
            )
        ),
        )
    )
    is_published = models.BooleanField(
        'Опубликовано', default=True, blank=True
    )
    created_at = models.DateTimeField(
        'Добавлено', auto_now_add=True)

    class Meta:
        default_related_name = 'recipes'
        ordering = ['-created_at']
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:constants.RESTRICTION_STRING]


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(MinValueValidator(
            constants.MINIMUM_AMOUNT_INGREDIENTS,
            message=(
                'Минимальное количество ингредиентов'
                f'{constants.MINIMUM_AMOUNT_INGREDIENTS}'
            )),
        )
    )

    class Meta:
        ordering = ['recipe']
        default_related_name = 'ingredient_recipes'
        verbose_name = 'количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'Колличество игредиента в {self.recipe}'


class Cart(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['author']
        default_related_name = 'carts'
        verbose_name = 'корзину'
        verbose_name_plural = 'Список карзин'
        constraints = [
            models.UniqueConstraint(fields=['author', 'recipe'],
                                    name='unique_author_recipe')
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.author}'


class Favorite(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        ordering = ['author']
        default_related_name = 'favorites'
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.author}'
