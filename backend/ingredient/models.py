from django.db import models

from foodgram import constants


class Ingredient(models.Model):
    name = models.CharField(
        'Название', max_length=constants.MAX_LENGTH
    )
    measurement_unit = models.CharField(
        'Единица измерения', max_length=constants.MAX_LENGTH
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Игредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_name_measurement_unit')
        ]

    def __str__(self):
        return self.name[:constants.RESTRICTION_STRING]
