# -*- coding: utf-8 -*-


# Есть функция генерации списка простых чисел


def get_prime_numbers(count_number):
    prime_numbers = []
    for num in range(2, count_number + 1):
        for prime in prime_numbers:
            if num % prime == 0:
                break
        else:
            prime_numbers.append(num)
    return prime_numbers

# Часть 1
# На основе алгоритма get_prime_numbers создать класс итерируемых обьектов,
# который выдает последовательность простых чисел до n
#
# Распечатать все простые числа до 10000 в столбик


class PrimeNumbers:

    def __init__(self, n):
        self.n = n
        self.number = []

    def __iter__(self):
        self.i = 1
        return self

    def _check_number(self):
        self.i += 1
        for prime in self.number:
            if self.i % prime == 0:
                return False
        return True

    def __next__(self):
        while self.i < self.n:
            if self._check_number():
                self.number.append(self.i)
                return self.i
        else:
            raise StopIteration()


# prime_number_iterator = PrimeNumbers(n=10000)
# for number in prime_number_iterator:
#     print(number)


#  после подтверждения части 1 преподователем, можно делать

# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик
def check(i, prime_num):
    for prime in prime_num:
        if i % prime == 0:
            return False
    return True


def prime_numbers_generator(count_number):
    prime_numbers = []
    i = 1
    while i < count_number:
        i += 1
        if check(i, prime_numbers):
            prime_numbers.append(i)
            yield i


# for number in prime_numbers_generator(count_number=10000):
#     print(number)

# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True
# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.

def lucky_number(num):
    num = str(num)
    center = len(num) // 2
    if len(num) % 2 == 0:
        half = center
    else:
        half = center + 1
    sum1 = sum([int(x) for x in num[:center]])
    sum2 = sum([int(x) for x in num[half:]])
    if sum1 == sum2:
        return True
    return False


def palindrome(num):
    num = str(num)
    reverse = num[len(num)::-1]
    if num == reverse:
        return True
    return False


def morph_number(num):
    square = num ** 2
    num = str(num)
    square = str(square)
    if num in square:
        return True
    return False


def centered_hexagonal_number():
    number = 1
    i = 1
    while True:
        yield number
        i += 1
        number = 3 * i * (i - 1) + 1


def check_centered_hexagonal_number(num):
    hexagonal_number = centered_hexagonal_number()
    if num in hexagonal_number:
        return True
    return False


def check_number(gen, func):
    for num in gen:
        if func(num):
            yield num


function = [lucky_number, palindrome, morph_number]
# 1 способ
print("1 способ")
for f in function:
    print(f"\n{f.__name__}")
    result = [x for x in prime_numbers_generator(count_number=10000) if f(x)]
    print(result)


# 2 способ
print("\n 2 способ")
for f in function:
    print(f"\n{f.__name__}")
    for numb in check_number(prime_numbers_generator(count_number=10000), f):
        print(numb)


# 3 способ
def filter_prime_numbers_generator(count_number, func):
    prime_numbers = []
    i = 1
    while i < count_number:
        i += 1
        if check(i, prime_numbers):
            prime_numbers.append(i)
            if func(i):
                yield i


print("\n 3 способ")
for f in function:
    print(f"\n{f.__name__}")
    numbers = filter_prime_numbers_generator(count_number=10000, func=f)
    for numb in numbers:
        print(numb)


# 4 способ
print("\n 4 способ")
for f in function:
    print(f"\n{f.__name__}")
    print(list(filter(f, prime_numbers_generator(count_number=10000))))


# 5 способ
def filters_prime_numbers_generator(count_number, func=None):
    prime_numbers = []
    i = 1
    while i < count_number:
        i += 1
        if check(i, prime_numbers):
            prime_numbers.append(i)
            if func is None:
                yield i
            else:
                for fun in func:
                    if not fun(i):
                        break
                else:
                    yield i


print("\n 5 способ")
functions = [lucky_number, palindrome]
for numb in filters_prime_numbers_generator(count_number=10000, func=functions):
    print(numb)
