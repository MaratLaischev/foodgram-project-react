from random import randint


def default_color():
    color_1 = format(randint(16, 255), 'X')
    color_2 = format(randint(16, 255), 'X')
    color_3 = format(randint(16, 255), 'X')
    return f'#{color_1}{color_2}{color_3}'
