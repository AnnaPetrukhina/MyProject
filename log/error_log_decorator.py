# -*- coding: utf-8 -*-

# Написать декоратор, который будет логировать (записывать в лог файл)
# ошибки из декорируемой функции и выбрасывать их дальше.
#
# Имя файла лога - function_errors.log
# Формат лога: <имя функции> <параметры вызова> <тип ошибки> <текст ошибки>
# Лог файл открывать каждый раз при ошибке в режиме 'a'
import sys


def log_errors(func):
    def write_errors(*args, **kwargs):
        with open("function_errors.log", "a", encoding="utf-8") as f:
            try:
                func(*args, **kwargs)
            except Exception as e:
                type_exception = sys.exc_info()[0].__name__
                if args != () and kwargs != {}:
                    argument = f"с параметрами вызова {args}, {kwargs}"
                elif args != () and kwargs == {}:
                    argument = f"с параметрами вызова {args}"
                elif args == () and kwargs != {}:
                    argument = f"с параметрами вызова {kwargs}"
                else:
                    argument = f"без параметров"
                f.write(f"В функции {func.__name__} {argument} произошла ошибка "
                        f"{type_exception}: {e} \n")
                raise
    return write_errors


# Проверить работу на следующих функциях
@log_errors
def perky(param):
    return param / 0


@log_errors
def check_line(ln):
    name, email, age = ln.split(' ')
    if not name.isalpha():
        raise ValueError("it's not a name")
    if '@' not in email or '.' not in email:
        raise ValueError("it's not a email")
    if not 10 <= int(age) <= 99:
        raise ValueError('Age not in 10..99 range')


lines = [
    'Ярослав bxh@ya.ru 600',
    'Земфира tslzp@mail.ru 52',
    'Тролль nsocnzas.mail.ru 82',
    'Джигурда wqxq@gmail.com 29',
    'Земфира 86',
    'Равшан wmsuuzsxi@mail.ru 35',
]
for line in lines:
    try:
        check_line(line)
    except Exception as exc:
        print(f'Invalid format: {exc}')

try:
    perky(param=42)
except Exception as exc:
    print(f'Invalid format: {exc}')


# Усложненное задание (делать по желанию).
# Написать декоратор с параметром - именем файла
