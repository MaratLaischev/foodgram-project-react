from random import randint

MAX_LENGTH = 200
MINIMUM_COOKING_TIME = 1
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_USER = 150
DEFAULT_PAGE_SIZE_POGINATION = 5
RECIPES_LIMIT_DEFOLT = 1
RESTRICTION_STRING = 30


def default_color():
    color_1 = format(randint(16, 255), 'X')
    color_2 = format(randint(16, 255), 'X')
    color_3 = format(randint(16, 255), 'X')
    return f'#{color_1}{color_2}{color_3}'
