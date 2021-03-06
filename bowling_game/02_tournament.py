# -*- coding: utf-8 -*-

# Прибежал менеджер и сказал что нужно срочно просчитать протокол турнира по боулингу в файле tournament.txt
#
# Пример записи из лога турнира
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/
#   Татьяна	62334/6/4/44X361/X
#   Давид	--8/--8/4/8/-224----
#   Павел	----15623113-95/7/26
#   Роман	7/428/--4-533/34811/
#   winner is .........
#
# Нужно сформировать выходной файл tournament_result.txt c записями вида
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/    98
#   Татьяна	62334/6/4/44X361/X      131
#   Давид	--8/--8/4/8/-224----    68
#   Павел	----15623113-95/7/26    69
#   Роман	7/428/--4-533/34811/    94
#   winner is Татьяна

# Код обаботки файла расположить отдельном модуле, модуль bowling_game использовать для получения количества очков
# одного участника. Если захочется изменить содержимое модуля bowling_game - тесты должны помочь.
#
# Из текущего файла сделать консольный скрипт для формирования файла с результатами турнира.
# Параметры скрипта: --input <файл протокола турнира> и --output <файл результатов турнира>

import argparse

from tournament_bowling import GetResultTour

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The scoring tournament result of bowling .')
    parser.add_argument("--protocol", action="store_const", const="tournament.txt",
                        dest="protocol", required=True, help='Protocol of the tournament')
    parser.add_argument("--result", action="store_const", const="tournament_result.txt",
                        dest="result", required=True, help='Result of the tournament')
    parser.add_argument("--internal_rule", action="store_true",
                        dest="internal", help='Result of the tournament')
    args = parser.parse_args()
    if args.internal:
        if args.result == "tournament_result.txt":
            args.result = "internal_scoring_tournament_result.txt"
        get_result_tour = GetResultTour(file_result=args.protocol, file_out=args.result, internal_scoring=True)
    else:
        get_result_tour = GetResultTour(file_result=args.protocol, file_out=args.result)
    get_result_tour.run()


# Усложненное задание (делать по желанию)
#
# После обработки протокола турнира вывести на консоль рейтинг игроков в виде таблицы:
#
# +----------+------------------+--------------+
# | Игрок    |  сыграно матчей  |  всего побед |
# +----------+------------------+--------------+
# | Татьяна  |        99        |      23      |
# ...
# | Алексей  |        20        |       5      |
# +----------+------------------+--------------+
