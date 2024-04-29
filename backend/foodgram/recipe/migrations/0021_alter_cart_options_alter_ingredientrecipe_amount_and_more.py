# Generated by Django 4.2.11 on 2024-04-29 19:59

import colorfield.fields
import django.core.validators
from django.db import migrations, models
import recipe.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0020_alter_favorite_options_alter_favorite_author_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'default_related_name': 'carts', 'ordering': ['author'], 'verbose_name': 'корзину', 'verbose_name_plural': 'Список карзин'},
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минимальное количество ингредиентов1')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default=recipe.models.default_color, image_field=None, max_length=7, samples=None, unique=True, verbose_name='Цвет'),
        ),
    ]
