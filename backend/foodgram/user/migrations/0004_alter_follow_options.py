# Generated by Django 4.2.11 on 2024-04-26 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ['user'], 'verbose_name': 'подписчик', 'verbose_name_plural': 'Подписчики'},
        ),
    ]