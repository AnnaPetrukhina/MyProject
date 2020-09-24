# -*- coding: utf-8 -*-

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет две локации и один монстр
# (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...

import csv
import json
import logging
import re
from datetime import timedelta
from decimal import Decimal
from typing import Dict, Any

from termcolor import cprint

REMAINING_TIME = '123456.0987654321'
# если изначально не писать число в виде строки - теряется точность!
field_names = ['current_location', 'current_experience', 'current_date']


class ExitDungeon:

    """
    Нахождение выхода из подземелья.
    Используется python 3.8.5
    """

    def __init__(self, path_map_dungeon, path_out_file):
        """"
        :param path_map_dungeon json файл с картой подземелья
        :param path_out_file csv файл, в котором будет статистика игры
        """
        self.path_map_dungeon = path_map_dungeon
        self.out = path_out_file
        self.map_of_the_dungeon = dict()
        self.remaining_time = Decimal(REMAINING_TIME)
        self.player_move: Dict[str, Any] = {"location": ["Location_0"], "experienced": 0, "current_date": "0"}
        self.exit = False

    def get_out_file(self):
        """"
        Запись полученной статистики в csv файл
        """
        with open(self.out, 'w', newline='', encoding="utf-8") as out_file:
            writer = csv.DictWriter(out_file, fieldnames=['location', 'experienced', 'current_date'])
            writer.writeheader()
            writer.writerow(self.player_move)

    def start_the_game_again(self):
        """
        Начало игры заново.
        Вывод статистики за прошедшую игру и возвращение к началльным параметрам игры
        """
        log.debug("Начнем поиск выхода сначала")
        second = self.player_move['current_date']
        self.player_move['current_date'] = self.conversion_of_seconds(second=second)
        print(f"У Вас оставалось {self.remaining_time} секунд.\nВаша статистика {self.player_move}")
        self.remaining_time = Decimal('123456.0987654321')
        self.player_move = {"location": ["Location_0"], "experienced": 0, "current_date": "0"}
        self.run()

    def exit_the_game(self):
        """"
        Выход из игры.
        Вывод статистики и завершение игры
        """
        log.debug("Выход из игры")
        self.exit = True
        cprint("Вы не смогли выбраться из подземелья и решили сдаться!", color="red")
        second = self.player_move['current_date']
        self.player_move['current_date'] = self.conversion_of_seconds(second=second)
        print(f"У Вас оставалось {self.remaining_time} секунд.\nВаша статистика {self.player_move}")

    def finish_the_game(self):
        """
        Победа в игре.
        Вывод статистики и завершение игры
        """
        log.debug("Найден выход из подземелья")
        cprint("Поздравляем! Вы смогли выйти из подземелья до того как Вас затопило!", color="red")
        second = self.player_move['current_date']
        self.player_move['current_date'] = self.conversion_of_seconds(second=second)
        print(f"У Вас оставалось {self.remaining_time} секунд.\nВаша статистика {self.player_move}")
        self.exit = True

    def get_map(self):
        """
        Получение карты подземелья из json файла
        """
        with open(self.path_map_dungeon, 'r') as f:
            self.map_of_the_dungeon = json.load(f)

    def timing(self, now_time, player_spend_time):
        """
        Подсчет потраченного времени
        :param now_time время потраченное при этом действии
        :param player_spend_time время потраченное игроком за всю игру
        :return spend_time время потраченное игроком за всю игру с учетом данного действия
        :return time_remaining  оставшееся время
        """
        spend_time = Decimal(player_spend_time) + Decimal(now_time)
        time_remaining = Decimal(self.remaining_time) - Decimal(now_time)
        if time_remaining < 0:
            log.debug(f"Кончилось время")
            self.remaining_time = 0
            cprint("У Вас закончилось время! Вам не удалось найти выход! Вас затопило!", color="red")
            answer = input("Начать заново? Введите y/n >>> ")
            if answer == "y":
                self.start_the_game_again()
            else:
                self.exit_the_game()
        return spend_time, time_remaining

    @staticmethod
    def conversion_of_seconds(second):
        """
        Преобразование секунд в дни, часы, минуты
        :param second секунды, которые будут преозразованы
        :return время в днях, часах, минутах и секундах
        """
        float_date = float(second)
        return timedelta(seconds=float_date)

    def _exploring_the_level_map(self, now_location):
        """"
        Получение объектов в локации. Вывод их на консоль
        :param now_location словарь всех объектов в текущей локации
        :return action словарь возможных действий в локации
        :return mob список всех действий в текущей локации
        :return current_location название текущей локации
        """
        action = dict()
        mob = ""
        current_location = ""
        re_location = r'(\w+_[\w\d]?\d)_'
        for current_location, objects_in_the_location in now_location.items():
            log.debug(f"{objects_in_the_location}")
            mob = objects_in_the_location.copy()
            now_location = re.search(re_location, current_location)[1]
            cprint(f"\nВы находитесь в {now_location}", color='blue')
            cprint(f"У Вас {self.player_move['experienced']} опыта. Прошло "
                   f"{self.conversion_of_seconds(self.player_move['current_date'])} времени. "
                   f"До новоднения осталось {self.remaining_time} секунд.", color="yellow")
            print("Перед вами:")
            for i, choice_act in enumerate(objects_in_the_location):
                if isinstance(choice_act, dict):
                    # локация
                    action[str(i + 1)] = choice_act
                    log.debug(f"локация {choice_act}")
                    for k in choice_act.keys():
                        if k[0] == "H":
                            print(f"{i + 1}: Выход из подземелья {k}")
                        else:
                            print(f"{i + 1}: Локация {k}")
                else:
                    # монстр
                    log.debug(f"монстр {choice_act}")
                    action[str(i + 1)] = choice_act
                    print(f"{i + 1}: Монстр {choice_act}")
        index = len(action) + 1
        action[f"{index}"] = "Выйти из игры"
        print(f"{index}: {action[f'{index}']}")
        return action, mob, current_location

    def _checking_for_the_following_locations(self, action):
        """
        Проверка возможности идти дальше (наличие следующей локациии)
        :param action словарь возможных действий в локации
        """
        count_location = 0
        for i in action.values():
            if isinstance(i, dict):
                count_location += 1
        log.debug(f"количество локаций {count_location}")
        if count_location == 0:
            log.debug("тупик")
            cprint("Дальше идти некуда!", color="red")
            answer = input("Начать заново? Введите y/n >>> ")
            if answer == "y":
                self.start_the_game_again()
            else:
                self.exit_the_game()
                return False
        return True

    @staticmethod
    def selecting_action(action):
        """"
        Выбор действия пользователя
        :param action словарь возможных действий
        :return new_level выбранное действие
        """
        cprint("Что вы выбираете? Перейти в следующую локацию, биться с монстром или выйти из игры.",
               color="yellow")
        act = input("Выбирете дальнейшее действие: ")
        while act not in action:
            cprint("Такого действия нет, попробуйте снова", color="red")
            act = input("Выбирете дальнейшее действие: ")
        new_level = action[act]
        # log.debug(f"{new_level}")
        return new_level

    def choosing_monster(self, current_location, mob, now_action):
        """
        Выбор монстра
        :param current_location текущая локация
        :param mob все возможные действия в текущей локации
        :param now_action строка с монстром
        :return new_level словарь текущей локации без выбранного монстра
        """
        re_time = r'tm([\d+]*[\.]?\d+)'
        re_exp = r'exp(\d+)_'
        log.debug(f"выбор монстра")
        mob.remove(now_action)
        t = Decimal(re.search(re_time, now_action)[1])
        self.player_move['current_date'], self.remaining_time = self.timing(
            now_time=t,
            player_spend_time=self.player_move['current_date']
        )
        self.player_move["experienced"] += int(re.search(re_exp, now_action)[1])
        log.debug(f"получено {self.player_move['experienced']} опыта. Потрачено {t} секундю")
        new_level = {f"{current_location}": mob}
        # log.debug(f"удаление монстра из возможных действий {new_level}")
        return new_level

    def choosing_hatch(self, hatch):
        """
        Выбор выхода
        :param hatch строка с люком
        """
        re_time = r'tm([\d+]*[\.]?\d+)'
        re_hatch = r'(\w+)_'
        log.debug(f"найден люк")
        self.player_move["location"].append(re.search(re_hatch, hatch)[1])
        cprint("Вы нашли выход!", color="red")
        if self.player_move['experienced'] < 280:
            log.debug(f"недостаточно опыта для открытия люка")
            cprint(f"Вы не можете открыть люк. У Вас недостаточно опыта. Необходимо "
                   f"не менее 280 опыта, у Вас {self.player_move['experienced']}", color="red")
            answer = input("Начать заново? Введите y/n >>> ")
            if answer == "y":
                self.start_the_game_again()
            else:
                self.exit_the_game()
        else:
            t = Decimal(re.search(re_time, hatch)[1])
            log.debug(f"затрачно {t} секунд")
            self.player_move['current_date'], self.remaining_time = self.timing(
                now_time=t,
                player_spend_time=self.player_move['current_date'])
            self.finish_the_game()

    def choosing_location(self, location, actions_in_the_location):
        """
        Выбор новой локации
        :param location строка выбранной локации
        :param actions_in_the_location список действий в этой локации
        :return new_level словарь с действиями выбранной локации
        """
        re_time = r'tm([\d+]*[\.]?\d+)'
        re_location = r'(\w+_[\w\d]?\d)_'
        log.debug(f"выбор локации")
        self.player_move["location"].append(re.search(re_location, location)[1])
        t = Decimal(re.search(re_time, location)[1])
        log.debug(f"затрачно {t} секунд")
        self.player_move['current_date'], self.remaining_time = self.timing(
            now_time=t,
            player_spend_time=self.player_move['current_date'])
        new_level = {f"{location}": actions_in_the_location}
        # log.debug(f"получение следующей локации {new_level}")
        return new_level

    def move(self, now_location):
        """
        Передвижение по подземелью
        :param now_location словарь всех объектов в текущей локации
        :return new_level словарь всех объектов после выбора действия пользователя
        """
        action, mob, current_location = self._exploring_the_level_map(now_location)
        if not self._checking_for_the_following_locations(action):
            return
        new_level = self.selecting_action(action)
        if isinstance(new_level, str) and new_level == "Выйти из игры":
            log.debug(f"выбор выхода")
            self.exit_the_game()
        elif isinstance(new_level, str):
            new_level = self.choosing_monster(current_location, mob, new_level)
        else:
            for k, v in new_level.items():
                if k[0] == "H":
                    self.choosing_hatch(k)
                else:
                    new_level = self.choosing_location(k, v)
        return new_level

    def run(self):
        """
        Запуск игры
        """
        self.get_map()
        cprint(f"Начнем исследование подземелья!", color="green")
        new_level = self.move(self.map_of_the_dungeon)
        while not self.exit:
            new_level = self.move(new_level)
            log.debug(f"{new_level}\n{self.player_move}")
        self.get_out_file()


log = logging.getLogger('Dungeon')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("dungeon.log", 'w', 'utf-8', delay=True)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M')
fh.setFormatter(formatter)
log.addHandler(fh)

if __name__ == '__main__':
    file = 'rpg.json'
    file_out = 'result_game.csv'
    log.info(f'Начнем поиск выхода')
    exit_dungeon = ExitDungeon(file, file_out)
    exit_dungeon.run()
