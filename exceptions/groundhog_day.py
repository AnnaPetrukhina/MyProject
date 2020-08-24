# -*- coding: utf-8 -*-

# День сурка
#
# Напишите функцию one_day() которая возвращает количество кармы от 1 до 7
# и может выкидывать исключения:
# - IamGodError
# - DrunkError
# - CarCrashError
# - GluttonyError
# - DepressionError
# - SuicideError
# Одно из этих исключений выбрасывается с вероятностью 1 к 13 каждый день
#
# Функцию оберните в бесконечный цикл, выход из которого возможен только при накоплении
# кармы до уровня ENLIGHTENMENT_CARMA_LEVEL. Исключения обработать и записать в лог.
# При создании собственных исключений максимально использовать функциональность
# базовых встроенных исключений.

from random import randint, choice


class MainException(Exception):
    pass


class IamGodError(MainException):

    def __str__(self):
        return "IamGodError: Я Бог"


class DrunkError(MainException):

    def __str__(self):
        return "DrunkError: Напился"


class CarCrashError(MainException):

    def __str__(self):
        return "CarCrashError: Разбился на машине"


class GluttonyError(MainException):

    def __str__(self):
        return "GluttonyError: Обожрался"


class DepressionError(MainException):

    def __str__(self):
        return "DepressionError: Депрессия"


class SuicideError(MainException):

    def __str__(self):
        return "SuicideError: Суицид"


def one_day():
    rnd = randint(1, 13)
    karma = randint(1, 7)
    if rnd == 13:
        raise choice(errors)
    return karma


ENLIGHTENMENT_CARMA_LEVEL = 777

errors = [IamGodError, DrunkError, CarCrashError, GluttonyError, DepressionError, SuicideError]

total_karma = 0
with open('Error.log', 'w', encoding="utf-8") as ff:
    while total_karma <= ENLIGHTENMENT_CARMA_LEVEL:
        try:
            total_karma += one_day()
        except MainException as exc:
            ff.write(f"{exc} \n")
print(total_karma)
