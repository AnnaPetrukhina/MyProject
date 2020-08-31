# -*- coding: utf-8 -*-

# На основе своего кода из lesson_009/02_log_parser.py напишите итератор (или генератор)
# котрый читает исходный файл events.txt и выдает число событий NOK за каждую минуту
# <время> <число повторений>
#
# пример использования:
#
# grouped_events = <создание итератора/генератора>  # Итератор или генератор? выбирайте что вам более понятно
# for group_time, event_count in grouped_events:
#     print(f'[{group_time}] {event_count}')
#
# на консоли должно появится что-то вроде
#
# [2018-05-17 01:57] 1234


class Counter:

    def __init__(self, file_name):
        self.file_name = file_name
        self.count = 0
        self.line = ""

    def __iter__(self):
        with open(self.file_name, 'r', encoding='cp1251') as file:
            for line in file:
                if line[-4:-1] != "NOK":
                    continue
                day = line.find(":") + 3
                line = line[:day]
                if self.line != line:
                    if self.line != "":
                        yield self.line, self.count
                    self.line = line
                self.count += 1
        yield self.line, self.count


# grouped_events = Counter("events.txt")
# for group_time, event_count in grouped_events:
#     print(f'{group_time}] {event_count}')


def grouped(file_name):
    count_nok = 1
    with open(file_name, 'r') as ff:
        for line in ff:
            if line[-4:-1] == "NOK":
                day = line.find(":") + 3
                lin = line[:day]
                break
        for line in ff:
            if line[-4:-1] == "NOK":
                day = line.find(":") + 3
                now_line = line[:day]
                if now_line != lin:
                    yield lin, count_nok
                    count_nok = 0
                    lin = now_line
                count_nok += 1
    yield lin, count_nok


grouped_events = grouped("events.txt")
for group_time, event_count in grouped_events:
    print(f'{group_time}] {event_count}')
