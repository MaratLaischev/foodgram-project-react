# Generated by Django 4.2.11 on 2024-04-18 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0012_rename_auther_cart_author_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'карзина', 'verbose_name_plural': 'Список карзин'},
        ),
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'тег', 'verbose_name_plural': 'Теги'},
        ),
    ]
