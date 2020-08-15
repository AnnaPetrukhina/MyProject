# -*- coding: utf-8 -*-

# Создать прототип игры Алхимия: при соединении двух элементов получается новый.
# Реализовать следующие элементы: Вода, Воздух, Огонь, Земля, Шторм, Пар, Грязь, Молния, Пыль, Лава.
# Каждый элемент организовать как отдельный класс.
# Таблица преобразований:
#   Вода + Воздух = Шторм
#   Вода + Огонь = Пар
#   Вода + Земля = Грязь
#   Воздух + Огонь = Молния
#   Воздух + Земля = Пыль
#   Огонь + Земля = Лава

# Сложение элементов реализовывать через __add__
# Если результат не определен - то возвращать None
# Вывод элемента на консоль реализовывать через __str__
#
# Примеры преобразований:
#   print(Water(), '+', Air(), '=', Water() + Air())
#   print(Fire(), '+', Air(), '=', Fire() + Air())


class Water:

    def __str__(self):
        return "Вода"

    def __add__(self, other):
        if isinstance(other, Air):
            return Gale(part1=self, part2=other)
        elif isinstance(other, Fire):
            return Vapor(part1=self, part2=other)
        elif isinstance(other, Sod):
            return Mud(part1=self, part2=other)
        elif isinstance(other, Existence):
            return Alga(part1=self, part2=other)
        else:
            return f"Сложение {self} и {other} ничего не дает"


class Fire:

    def __str__(self):
        return "Огонь"

    def __add__(self, other):
        if isinstance(other, Air):
            return Lighting(part1=self, part2=other)
        elif isinstance(other, Water):
            return Vapor(part1=self, part2=other)
        elif isinstance(other, Sod):
            return Lava(part1=self, part2=other)
        else:
            return f"Сложение {self} и {other} ничего не дает"


class Air:

    def __str__(self):
        return "Воздух"

    def __add__(self, other):
        if isinstance(other, Fire):
            return Lighting(part1=self, part2=other)
        elif isinstance(other, Water):
            return Gale(part1=self, part2=other)
        elif isinstance(other, Sod):
            return Dust(part1=self, part2=other)
        elif isinstance(other, Existence):
            return Bird(part1=self, part2=other)
        else:
            return f"Сложение {self} и {other} ничего не дает"


class Sod:

    def __str__(self):
        return "Земля"

    def __add__(self, other):
        if isinstance(other, Fire):
            return Lava(part1=self, part2=other)
        elif isinstance(other, Water):
            return Mud(part1=self, part2=other)
        elif isinstance(other, Air):
            return Dust(part1=self, part2=other)
        elif isinstance(other, Existence):
            return Seed(part1=self, part2=other)
        else:
            return f"Сложение {self} и {other} ничего не дает"


class Gale:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return "Шторм"

    def __add__(self, other):
        return f"Сложение {self} и {other} ничего не дает"


class Vapor:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return "Пар"

    def __add__(self, other):
        return f"Сложение {self} и {other} ничего не дает"


class Mud:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return "Грязь"

    def __add__(self, other):
        if isinstance(other, Lighting):
            return Existence(part1=self, part2=other)
        else:
            return f"Сложение {self} и {other} ничего не дает"


class Lighting:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return "Молния"

    def __add__(self, other):
        return f"Сложение {self} и {other} ничего не дает"


class Dust:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return "Пыль"

    def __add__(self, other):
        return f"Сложение {self} и {other} ничего не дает"


class Lava:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return "Лава"

    def __add__(self, other):
        return f"Сложение {self} и {other} ничего не дает"


class Existence:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return "Жизнь"

    def __add__(self, other):
        if isinstance(other, Air):
            return Bird(part1=self, part2=other)
        elif isinstance(other, Water):
            return Alga(part1=self, part2=other)
        elif isinstance(other, Sod):
            return Seed(part1=self, part2=other)
        else:
            return f"Сложение {self} и {other} ничего не дает"


class Bird:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return "Птица"

    def __add__(self, other):
        return f"Сложение {self} и {other} ничего не дает"


class Alga:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return "Водоросли"

    def __add__(self, other):
        return f"Сложение {self} и {other} ничего не дает"


class Seed:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return "Семя"

    def __add__(self, other):
        return f"Сложение {self} и {other} ничего не дает"


elements = {"water": Water(), "fire": Fire(), "air": Air(), "sod": Sod(), "gale": Gale(Water, Air),
            "vapor": Vapor(Fire, Water), "mud": Mud(Sod, Water), "lighting": Lighting(Fire, Air),
            "dust": Dust(Air, Sod), "lava": Lava(Fire, Sod)}

print(elements["water"], '+', elements["air"], '=', elements["water"] + elements["air"])
print(elements["water"], '+', elements["fire"], '=', elements["water"] + elements["fire"])
print(elements["water"], '+', elements["sod"], '=', elements["water"] + elements["sod"])
print("------------------------------")
print(elements["fire"], '+', elements["air"], '=', elements["fire"] + elements["air"])
print(elements["fire"], '+', elements["water"], '=', elements["fire"] + elements["water"])
print(elements["fire"], '+', elements["sod"], '=', elements["fire"] + elements["sod"])
print("------------------------------")
print(elements["air"], '+', elements["fire"], '=', elements["air"] + elements["fire"])
print(elements["air"], '+', elements["water"], '=', elements["air"] + elements["water"])
print(elements["air"], '+', elements["sod"], '=', elements["air"] + elements["sod"])
print("------------------------------")
print(elements["sod"], '+', elements["fire"], '=', elements["sod"] + elements["fire"])
print(elements["sod"], '+', elements["water"], '=', elements["sod"] + elements["water"])
print(elements["sod"], '+', elements["air"], '=', elements["sod"] + elements["air"])
print("------------------------------")
print(elements["sod"], '+', elements["sod"], '=', elements["sod"] + elements["sod"])
print(elements["sod"], '+', elements["dust"], '=', elements["sod"] + elements["dust"])
print("------------------------------")

# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.

print(Mud(Sod, Water), '+', Lighting(Fire, Air), '=', Mud(Sod, Water) + Lighting(Fire, Air))
# сделала специально сложение в одну сторону, т.е. не работает перемистительный закон
print(Lighting(Fire, Air), '+', Mud(Sod, Water), '=', Lighting(Fire, Air) + Mud(Sod, Water))
print(Existence(Mud, Lighting), '+', elements["air"], '=', Existence(Mud, Lighting) + elements["air"])
print(Existence(Mud, Lighting), '+', elements["water"], '=', Existence(Mud, Lighting) + elements["water"])
print(Existence(Mud, Lighting), '+', elements["sod"], '=', Existence(Mud, Lighting) + elements["sod"])
