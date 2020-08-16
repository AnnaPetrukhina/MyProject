# -*- coding: utf-8 -*-
from random import randint, choice

from termcolor import cprint


# Необходимо создать класс кота. У кота есть аттрибуты - сытость и дом (в котором он живет).
# Кот живет с человеком в доме.
# Для кота дом характеризируется - миской для еды и грязью.
# Изначально в доме нет еды для кота и нет грязи.

# Доработать класс человека, добавив методы
#   подобрать кота - у кота появляется дом.
#   купить коту еды - кошачья еда в доме увеличивается на 50, деньги уменьшаются на 50.
#   убраться в доме - степень грязи в доме уменьшается на 100, сытость у человека уменьшается на 20.
# Увеличить кол-во зарабатываемых человеком денег до 150 (он выучил пайтон и устроился на хорошую работу :)

# Кот может есть, спать и драть обои - необходимо реализовать соответствующие методы.
# Когда кот спит - сытость уменьшается на 10
# Когда кот ест - сытость увеличивается на 20, кошачья еда в доме уменьшается на 10.
# Когда кот дерет обои - сытость уменьшается на 10, степень грязи в доме увеличивается на 5
# Если степень сытости < 0, кот умирает.
# Так же надо реализовать метод "действуй" для кота, в котором он принимает решение
# что будет делать сегодня

# Человеку и коту надо вместе прожить 365 дней.


class Man:

    def __init__(self, name):
        self.name = name
        self.fullness = 50
        self.house = None
        self.cat = None

    def __str__(self):
        return f'Я - {self.name}, сытость {self.fullness}'

    def eat(self):
        if self.house.food >= 10:
            cprint(f'{self.name} поел', color='yellow')
            self.fullness += 10
            self.house.food -= 10
        else:
            cprint(f'{self.name} нет еды', color='red')

    def work(self):
        cprint(f'{self.name} сходил на работу', color='blue')
        self.house.money += 150
        self.fullness -= 20

    def watch_tv(self):
        cprint(f'{self.name} смотрел телевизор целый день', color='green')
        self.fullness -= 10

    def shopping(self):
        if self.house.money >= 50:
            cprint(f'{self.name} сходил в магазин за едой', color='magenta')
            self.house.money -= 50
            self.house.food += 50
        else:
            cprint(f'{self.name} деньги кончились!', color='red')

    def shopping_cat(self):
        if self.house.money >= 50:
            cprint(f'{self.name} сходил в магазин за едой для кошки', color='magenta')
            self.house.money -= 50
            self.house.food_cat += 50
        else:
            cprint(f'{self.name} деньги кончились!', color='red')

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint(f'{self.name} Вьехал в дом', color='cyan')

    def get_cat(self, kitty):
        name_cats = ["Барсик", "Буся", "Рыжик", "Пуся", "Сима", "Дымка", "Персик", "Матильда"]
        self.cat = kitty
        self.cat.owner = self.name
        self.cat.house = self.house
        self.cat.name = choice(name_cats)
        cprint(f"{self.name} завел кота {self.cat.name}", color='magenta')

    def clear_house(self):
        self.house.mud -= 100
        if self.house.mud < 0:
            self.house.mud = 0
        self.fullness -= 20
        cprint(f'{self.name} убрал дом', color='blue')

    def act(self):
        if self.fullness <= 0:
            cprint(f'{self.name} умер...', color='red')
            return "dead"
        dice = randint(1, 6)
        if self.house.money <= 50:
            self.work()
        elif self.house.food <= 10:
            self.shopping()
        elif self.fullness <= 30:
            self.eat()
        elif self.house.food_cat <= 10:
            self.shopping_cat()
        elif self.house.mud > 100:
            self.clear_house()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        elif dice == 3:
            self.clear_house()
        else:
            self.watch_tv()


class House:

    def __init__(self):
        self.food = 50
        self.money = 0
        self.food_cat = 0
        self.mud = 0

    def __str__(self):
        return f'В доме осталось: \n- еды {self.food} \n- кошачьей еды {self.food_cat} \n- денег {self.money} ' \
               f'\nГрязь в доме {self.mud}'


class Cat:

    def __init__(self):
        self.name = "У меня пока нет имени"
        self.fullness = 50
        self.house = None
        self.owner = "У меня пока нет хозяина"

    def eat(self):
        if self.house.food_cat >= 10:
            cprint(f'{self.name} поел', color='yellow')
            self.fullness += 20
            self.house.food_cat -= 10
        else:
            cprint(f'У {self.name} нет еды', color='red')

    def sleep(self):
        cprint(f'{self.name} поспал', color='green')
        self.fullness -= 10

    def tear_up_wallpaper(self):
        cprint(f"{self.name} дерет обои", color='yellow')
        self.fullness -= 10
        self.house.mud += 5

    def meow(self):
        cprint(f"{self.name} просит еды", color='red')

    def act(self):
        if self.fullness <= 0:
            cprint(f'{self.name} умер...', color='red')
            return
        dice = randint(1, 6)
        if self.fullness <= 10:
            self.eat()
        elif self.house.food_cat < 10:
            self.meow()
        elif dice == 1:
            self.tear_up_wallpaper()
        elif dice == 2:
            self.eat()
        else:
            self.sleep()

    def __str__(self):
        return f'Я - {self.name}, сытость {self.fullness}, мой хозяин {self.owner}'


def kittens(count):
    kitties = []
    for _ in range(count):
        kitties.append(Cat())
    return kitties


def year_with_few_cats(inhabitants, citizens_cats, range_count_cat):
    for i, inhabitant in enumerate(inhabitants):
        inhabitant.go_to_the_house(house=my_sweet_home)
        count_cat = randint(1, range_count_cat)
        if count_cat != 0:
            citizens_cats.append(kittens(count=count_cat))
            for kitty_cat in citizens_cats[i]:
                inhabitant.get_cat(kitty=kitty_cat)
    state = ""
    for day in range(1, 366):
        print(f'================ день {day} ==================')
        for inhabitant in inhabitants:
            state_of_man = inhabitant.act()
            if state_of_man == "dead":
                state = "brake"
        for citizen_cat in citizens_cats:
            for kitty_cat in citizen_cat:
                kitty_cat.act()
        print('--- в конце дня ---')
        for inhabitant in inhabitants:
            print(inhabitant)
        for citizen_cat in citizens_cats:
            for kitty_cat in citizen_cat:
                print(kitty_cat)
        print(my_sweet_home)
        if state == "brake":
            break


citizens = [
    Man(name='Бивис')]

cat = Cat()
my_sweet_home = House()
answer = input("Хотите увидеть как живет один человек с котом? Введите yes, если хотите >>> ")
if answer == "yes":
    for citizen in citizens:
        citizen.go_to_the_house(house=my_sweet_home)
        citizen.get_cat(kitty=cat)

    for daytime in range(1, 366):
        print(f'================ день {daytime} ==================')
        for citizen in citizens:
            citizen.act()
        cat.act()
        print('--- в конце дня ---')
        for citizen in citizens:
            print(citizen)
        print(cat)
        print(my_sweet_home)

# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)
answer = input("Хотите увидеть как живет один человек с случайным числом котов? Введите yes, если хотите. >>> ")
if answer == "yes":
    year_with_few_cats(inhabitants=citizens, citizens_cats=[], range_count_cat=15)

citizens.append(Man(name="Батхед"))
citizens.append(Man(name="Пушкин"))
answer = input("Хотите увидеть как живет несколько человек с случайным числом котов? Введите yes, если хотите. >>> ")
if answer == "yes":
    year_with_few_cats(inhabitants=citizens, citizens_cats=[], range_count_cat=4)
