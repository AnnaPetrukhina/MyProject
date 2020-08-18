import itertools
from random import sample

from family import Husband, Wife, Cat, Child, House
from termcolor import cprint


def simulation(money_incident, food_incident, sal):
    count_death = 0
    count_kitty = 0
    kitties = []
    serge.salary = sal
    day_food_incidents = sample(range(365), food_incident)
    day_money_incidents = sample(range(365), money_incident)
    while count_death < 2:
        count_kitty += 1
        kitty = Cat()
        kitties.append(kitty)
        masha.get_cat(kitty=kitty)
        serge.get_cat(kitty=kitty)
        count_experiment = 0
        while count_experiment < 3:
            count_experiment += 1
            for daytime in range(366):
                if daytime in day_food_incidents:
                    home.food /= 2
                if daytime in day_money_incidents:
                    home.money /= 2
                serge.act()
                masha.act()
                kolya.act()
                for kitty in kitties:
                    kitty.act()
                if serge.state == "dead" or masha.state == "dead" or kolya.state == "dead":
                    count_death += 1
                    break
    return count_kitty


home = House()
serge = Husband(name='Сережа')
serge.go_to_the_house(house=home)
masha = Wife(name='Маша')
masha.go_to_the_house(house=home)
kolya = Child(name='Коля')
kolya.go_to_the_house(house=home)

for food_incidents, money_incidents in itertools.product(range(6), range(6)):
    cprint(f"Эксперимент с пропаданием половина еды {food_incidents} раз, "
           f"пропаданием половины денег {money_incidents} раз", color="blue")
    for salary in range(50, 401, 50):
        home.new_experiment()
        serge.new_experiment()
        masha.new_experiment()
        kolya.new_experiment()
        cprint(f"с зарплатой {salary}", color="yellow")
        max_cats = simulation(money_incident=money_incidents, food_incident=food_incidents, sal=salary)
        print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов \n')
