# -*- coding: utf-8 -*-

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.
import zipfile
from collections import defaultdict
from operator import itemgetter
from prettytable import PrettyTable


class Statistic:

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat = defaultdict(int)
        self._type_sorting = {"sort_frequency_decrease": [itemgetter(1), True],
                              "sort_frequency_increase": [itemgetter(1), False],
                              "sort_alphabet_decrease": [itemgetter(0), True],
                              "sort_alphabet_increase": [itemgetter(0), False]}

    def unzip(self):
        zfile = zipfile.ZipFile(self.file_name, 'r')
        for filename in zfile.namelist():
            zfile.extract(filename)
            self.file_name = filename

    def collect(self):
        if self.file_name.endswith('.zip'):
            self.unzip()
        with open(self.file_name, 'r', encoding='cp1251') as file:
            for line in file:
                self._collect_for_line(line=line[:-1])

    def _collect_for_line(self, line):
        for char in line:
            if char.isalpha():
                self.stat[char] += 1

    def sort(self, sort):
        sorted_list = sorted(self.stat.items(), key=self._type_sorting[sort][0],
                             reverse=self._type_sorting[sort][1])
        self.stat = dict(sorted_list)

    def frequency(self, out_file_name=None):
        if out_file_name is not None:
            file = open(out_file_name, 'w', encoding='utf8')
        else:
            file = None
        frequency_table = PrettyTable()
        frequency_table.field_names = ["Буква", "Частота"]
        count = 0
        for key, value in self.stat.items():
            count += value
            frequency_table.add_row([f"{key:^30}", f"{value:^30}"])
        frequency_table.add_row([f"{'':-^30}", f"{'':-^30}"])
        frequency_table.add_row([f"{'Итог':^30}", f"{count:^30}"])
        print(frequency_table, file=file)
        if file:
            file.close()


type_sorting = {"Упорядочить статистику по убыванию частоты (y/n)? >>> ":
                ["out_sort_frequency_decrease.txt", "sort_frequency_decrease"],
                "Упорядочить статистику по возрастанию частоты (y/n)? >>> ":
                ["out_sort_frequency_increase.txt", "sort_frequency_increase"],
                "Упорядочить статистику по убыванию алфавита (y/n)? >>> ":
                ["out_sort_alphabet_decrease.txt", "sort_alphabet_decrease"],
                "Упорядочить статистику по возрастанию алфавита (y/n)? >>> ":
                ["out_sort_alphabet_increase.txt", "sort_alphabet_increase"]}


statistic = Statistic(file_name='voyna-i-mir.txt.zip')
statistic.collect()
for offer, sorting in type_sorting.items():
    answer = input(f"{offer}")
    if answer == "y":
        statistic.sort(sorting[1])
        answer = input("Записать результат в файл (y/n)? >>> ")
        if answer == "y":
            statistic.frequency(out_file_name=f'{sorting[0]}')
        else:
            statistic.frequency()


# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4
