# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.
import collections


class Counter:

    def __init__(self, file_name, out_file_name):
        self.file_name = file_name
        self.out_file_name = out_file_name
        self.statistic = collections.defaultdict(int)
        self._type_collecting = {"collecting_minutes": [":", 3],
                                 "collecting_hours": [" ", 3],
                                 "collecting_days": [" ", 0],
                                 "collecting_months": ["-", 3],
                                 "collecting_years": ["-", 0]}

    def _counter(self, line, delimiter, move):
        if line[-4:-1] == "NOK":
            day = line.find(delimiter) + move
            now_line = line[:day]
            self.statistic[now_line] += 1

    def _out(self, out=None):
        if out is not None:
            self.out_file_name = out
        count_nok = 0
        with open(self.out_file_name, 'w', encoding='cp1251') as out_file:
            for year, count in self.statistic.items():
                count_nok += count
                out_file.write(f"{year}] {count_nok} \n")
        self.statistic = collections.defaultdict(int)

    def collecting_nok(self, grouping, out=None):
        with open(self.file_name, 'r', encoding='cp1251') as file:
            for line in file:
                self._counter(line, delimiter=self._type_collecting[grouping][0],
                              move=self._type_collecting[grouping][1])
            self._out(out)


def selection():
    user_input = input(f"Введите номер желаемой группировки >>> ")
    while user_input not in type_collecting:
        print("Вы ввели некорректный номер, попробуйте ввести другой номер")
        user_input = input(f"Введите номер желаемой группировки >>> ")
    return user_input


nok = Counter("events.txt", "count_NOK.txt")
type_collecting = {"1": ["Сгруппировать статистику по минутам", "out_collecting_minutes.txt", "collecting_minutes"],
                   "2": ["Сгруппировать статистику по часам", "out_collecting_hours.txt", "collecting_hours"],
                   "3": ["Сгруппировать статистику по дням", "out_collecting_days.txt", "collecting_days"],
                   "4": ["Сгруппировать статистику по месецам", "out_collecting_months.txt", "collecting_months"],
                   "5": ["Сгруппировать статистику по годам", "out_collecting_years.txt", "collecting_years"]}

print("Выберите способ группировки:")
for number, collect in type_collecting.items():
    print(f"{number}. {collect[0]}")
number_collecting = selection()
collecting = type_collecting[number_collecting][2]
name_out_file = type_collecting[number_collecting][1]
nok.collecting_nok(f"{collecting}", f"{name_out_file}")

# После выполнения первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4
