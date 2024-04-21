from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

# from user.models import User
# from ingredient.models import IngredientRecipe


User = get_user_model()
# https://practicum.yandex.ru/trainer/backend-developer/lesson/33b6ddf0-f6a3-42de-bce4-69e5321cff55/?searchedText=список
# Оптимизация запросов к бд


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('HEX-код', max_length=7, default='#FF0000')
    slug = models.SlugField('Уникальный слаг', max_length=200, unique=True)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='recipes'
    )
    name = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка', upload_to='recipe_img/', blank=True)
    text = models.TextField('Описание')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в мин.',
        validators=(MinValueValidator(
            1, message='Минимальное время приготовления 1 минута'),
        )
    )
    is_published = models.BooleanField(
        'Опубликовано', default=True, blank=True
    )
    created_at = models.DateTimeField(
        'Добавлено', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Cart(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cart'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='cart'
    )

    class Meta:
        verbose_name = 'карзину'
        verbose_name_plural = 'Список карзин'

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.author}'


class Favorite(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites'
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.author}'
