# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.


class NotNameError(Exception):
    pass


class NotEmailError(Exception):
    pass


def check_user(now_line):
    name_user, email_user, age_user = now_line.split(' ')
    if not name_user.isalpha():
        raise NotNameError
    elif "." not in email_user and "@" not in email_user:
        raise NotEmailError
    elif int(age_user) < 10 or int(age_user) > 99:
        raise ValueError("Wrong age")


with open('registrations.txt', 'r', encoding="utf-8") as f, \
        open('registrations_good.log', 'w', encoding="utf-8") as good_f, \
        open('registrations_bad.log', 'w', encoding="utf-8") as bad_f:
    for line in f:
        try:
            check_user(line)
            good_f.write(f"{line}")
        except ValueError as exc:
            if 'unpack' in exc.args[0]:
                pass
                bad_f.write(f'Не хватает данных {exc} в строке {line}')
            else:
                pass
                bad_f.write(f'Введен некорректный возраст в строке {line}')
        except NotNameError as exc:
            pass
            bad_f.write(f'Неправильно введено имя в строке {line}')
        except NotEmailError as exc:
            pass
            bad_f.write(f'Неправильно введен имейл в строке {line}')
