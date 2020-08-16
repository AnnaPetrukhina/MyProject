# -*- coding: utf-8 -*-
from random import randint, choice

from termcolor import cprint


# Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умирает от депрессии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:

    def __init__(self):
        self.food = 50
        self.money = 100
        self.mud = 0
        self.food_cat = 30

    def end_day(self):
        self.mud += 5

    def __str__(self):
        return f'В доме осталось: \n- еды {self.food} \n- кошачьей еды {self.food_cat} \n- денег {self.money} ' \
               f'\nГрязь в доме {self.mud}'

    def new_experiment(self):
        self.food = 50
        self.money = 100
        self.mud = 0
        self.food_cat = 30


class Man:
    money_earned = 0
    food_eaten = 0
    count_coat = 0
    state = "live"
    cat = None

    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.house = None
        self.cats = []

    def __str__(self):
        return f'Я - {self.name}, сытость {self.fullness}, счастье {self.happiness}'

    def new_experiment(self):
        self.fullness = 30
        self.happiness = 100
        Man.state = "live"
        self.cats = []

    def eat(self):
        if self.house.food > 30:
            self.fullness += 30
            self.house.food -= 30
            Man.food_eaten += 30
        elif self.house.food > 20:
            self.fullness += 20
            self.house.food -= 20
            Man.food_eaten += 20
        elif self.house.food >= 10:
            self.fullness += 10
            self.house.food -= 10
            Man.food_eaten += 10
        elif __name__ == "__main__":
            cprint(f'{self.name} нет еды', color='red')
            return False
        return True

    def work(self):
        self.house.money += 150
        Man.money_earned += 150
        self.fullness -= 10
        self.happiness -= 10

    def gaming(self):
        self.fullness -= 10
        self.happiness += 20

    def shopping_eat(self):
        if self.house.money >= 50:
            self.house.money -= 50
            self.house.food += 50
            self.fullness -= 10
        elif self.house.money >= 20:
            self.house.money -= 20
            self.house.food += 20
            self.fullness -= 10
        elif __name__ == "__main__":
            cprint(f'{self.name} деньги кончились!', color='red')
            self.fullness -= 10
            return False
        return True

    def shopping_coat(self):
        if self.house.money >= 360:
            self.house.money -= 350
            self.fullness -= 10
            self.happiness += 60
            Man.count_coat += 1
            return True
        elif __name__ == "__main__":
            cprint(f'{self.name} денег на шубу нет!', color='red')
            return False

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        if __name__ == "__main__":
            cprint(f'{self.name} Вьехал в дом', color='cyan')

    def clear_house(self):
        self.house.mud -= 100
        if self.house.mud < 0:
            self.house.mud = 0
        self.fullness -= 10
        self.happiness -= 10

    def get_cat(self, kitty):
        name_cats = ["Барсик", "Буся", "Рыжик", "Пуся", "Сима", "Дымка", "Персик", "Матильда"]
        Man.cat = kitty
        if len(Man.cat.owner) == 0:
            Man.cat.owner.append(self.name)
            Man.cat.house = self.house
            Man.cat.name = choice(name_cats)
        else:
            Man.cat.owner.append(self.name)
        if __name__ == "__main__":
            cprint(f"{self.name} завел кота {Man.cat.name}", color='magenta')
        self.cats.append(Man.cat)

    def pet_cat(self):
        self.happiness += 5

    def shopping_cat(self):
        if self.house.money >= 20 * len(self.cats):
            self.house.money -= 20 * len(self.cats)
            self.house.food_cat += 20 * len(self.cats)
            return True
        elif self.house.money >= 50:
            self.house.money -= 50
            self.house.food_cat += 50
            return True
        elif __name__ == "__main__":
            cprint(f'{self.name} деньги кончились!', color='red')
            return False

    def act(self):
        if self.fullness <= 0 or self.happiness <= 10:
            Man.state = "dead"
            return False
        return True


class Husband(Man):

    def act(self):
        if super().act():
            if self.house.mud >= 90:
                self.happiness -= 10
            dice = randint(1, 6)
            if self.house.money <= 100:
                self.work()
            elif self.fullness <= 30:
                self.eat()
            elif self.happiness < 15:
                self.gaming()
            elif dice == 1:
                self.work()
            elif dice == 2:
                self.eat()
            elif dice == 3:
                self.pet_cat()
            else:
                self.gaming()
        elif __name__ == "__main__":
            cprint(f'{self.name} умер...', color='red')

    def eat(self):
        if super().eat() and __name__ == "__main__":
            # if __name__ == "__main__":
            cprint(f'{self.name} поел', color='yellow')

    def work(self):
        super().work()
        if __name__ == "__main__":
            cprint(f'{self.name} сходил на работу', color='blue')

    def gaming(self):
        super().gaming()
        if __name__ == "__main__":
            cprint(f'{self.name} играл целый день', color='green')

    def pet_cat(self):
        super().pet_cat()
        if __name__ == "__main__":
            cprint(f'{self.name} погладил кота', color='green')


class Wife(Man):

    def act(self):
        if super().act():
            if self.house.mud >= 90:
                self.happiness -= 10
            dice = randint(1, 6)
            if self.house.food <= 20:
                self.shopping()
            elif self.fullness <= 30:
                self.eat()
            elif self.house.food_cat <= 10:
                self.shopping_cat()
            elif self.house.mud >= 90:
                self.clean_house()
            elif self.happiness <= 20:
                self.buy_fur_coat()
            elif self.happiness <= 15:
                self.pet_cat()
            elif dice == 1:
                self.eat()
            elif dice == 2:
                self.clean_house()
            elif dice == 3:
                self.pet_cat()
            else:
                self.buy_fur_coat()
        elif __name__ == "__main__":
            cprint(f'{self.name} умерла...', color='red')

    def eat(self):
        if super().eat() and __name__ == "__main__":
            # if __name__ == "__main__":
            cprint(f'{self.name} поела', color='yellow')

    def shopping(self):
        if super().shopping_eat() and __name__ == "__main__":
            # if __name__ == "__main__":
            cprint(f'{self.name} сходила в магазин за едой', color='magenta')

    def shopping_cat(self):
        if super().shopping_cat() and __name__ == "__main__":
            # if __name__ == "__main__":
            cprint(f'{self.name} сходила в магазин за кошачьей едой', color='magenta')

    def buy_fur_coat(self):
        if super().shopping_coat() and __name__ == "__main__":
            # if __name__ == "__main__":
            cprint(f'{self.name} купила шубу', color='magenta')

    def clean_house(self):
        super().clear_house()
        if __name__ == "__main__":
            cprint(f'{self.name} убрала дом', color='blue')

    def pet_cat(self):
        super().pet_cat()
        if __name__ == "__main__":
            cprint(f'{self.name} погладила кота', color='green')


home = House()
serge = Husband(name='Сережа')
serge.go_to_the_house(house=home)
masha = Wife(name='Маша')
masha.go_to_the_house(house=home)


for day in range(366):
    cprint(f'\n================== День {day} ==================', color='green')
    serge.act()
    masha.act()
    home.end_day()
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(f"\n{home}", color='cyan')
    if serge.state == "dead" or masha.state == "dead":
        break

print(f"\nЗа год заработано денег {serge.money_earned}, съедено еды {serge.food_eaten + masha.food_eaten}, "
      f"куплено шуб {masha.count_coat}")


# Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов


# Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)


# Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')
