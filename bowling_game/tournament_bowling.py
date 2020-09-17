import logging
from collections import defaultdict
from operator import itemgetter

from prettytable import PrettyTable

from bowling import GetScore, InternalGetScore


class GetResultTour:

    def __init__(self, file_result, file_out, internal_scoring=False):
        self.file = file_result
        self.file_out = file_out
        self.internal_scoring = internal_scoring
        self.max = 0
        self.winner = ""
        self.result_tournament = defaultdict(list)
        self.number_of_winner = defaultdict(int)
        self.matches_played = defaultdict(int)

    def add_out_file(self, line):
        with open(self.file_out, "a", encoding="utf-8") as f:
            f.write(line)

    def get_tour_players(self, line):
        name = line.split("\t")[0]
        self.matches_played[name] += 1
        result = line[:-1].split("\t")[1]
        try:
            if self.internal_scoring:
                score = InternalGetScore(result).run()
            else:
                score = GetScore(result).run()
            lg.debug(f"{name} {result} {score}")
            if score > self.max:
                self.max = score
                self.winner = name
            self.add_out_file(f"{name:<30} {result:^30} {score:^20}\n")
        except Exception as ex:
            lg.info(f"{ex} {name}")
            score = 0
            lg.debug(f"{name} {result} {score} {ex}")
            self.add_out_file(f"{name:<30} {result:^30} {score:^20} {ex}\n")

    def table_result_tournament(self):
        frequency_table = PrettyTable()
        frequency_table.field_names = ["Игрок", "сыграно матчей", "всего побед"]
        self.matches_played = dict(sorted(self.matches_played.items(), key=itemgetter(1), reverse=True))
        for name, count in self.matches_played.items():
            self.result_tournament[name].append(count)
            self.result_tournament[name].append(self.number_of_winner[name])
            frequency_table.add_row([f"{name:^30}", f"{count:^30}", f"{self.number_of_winner[name]:^30}"])
        print(frequency_table)

    def run(self):
        with open(self.file, "r", encoding="utf-8") as f:
            for line in f:
                if line[0] == "#":
                    lg.debug(line[:-1])
                    self.add_out_file(f"{line}")
                elif line[0] != "w" and line != "\n":
                    self.get_tour_players(line)
                elif line[0] == "w":
                    self.number_of_winner[self.winner] += 1
                    self.add_out_file(f"Winner is {self.winner}\n")
                else:
                    lg.debug(f"{self.winner}\n")
                    self.max = 0
                    self.winner = ""
        answer = input("Хотитите увидеть статистику турнира? Введите y/n >>> ")
        if answer == "y":
            self.table_result_tournament()


lg = logging.getLogger('Bowling_tournament')
lg.setLevel(logging.INFO)
fh = logging.FileHandler("errors_bowling_tournament.log", 'w', 'utf-8', delay=True)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M')
fh.setFormatter(formatter)
lg.addHandler(fh)


if __name__ == '__main__':
    file = "tournament.txt"
    file_internal_score = "internal_scoring_tournament_result.txt"
    file_score = "scoring_tournament_result.txt"
    get_internal_result_tour = GetResultTour(file_result=file, file_out=file_internal_score, internal_scoring=True)
    get_internal_result_tour.run()
    get_result_tour = GetResultTour(file_result=file, file_out=file_score)
    get_result_tour.run()
