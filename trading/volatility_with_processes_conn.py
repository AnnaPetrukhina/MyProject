# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
#
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#

from pathlib import Path
from multiprocessing import Process, Pipe
from sort import sort_ticker, time_track, generation_filename


class Ticker(Process):

    def __init__(self, file_name, conn,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = file_name
        self.volatility = 0
        self.name = ""
        self.conn = conn

    def run(self):
        with open(self.file, 'r') as ff:
            next(ff)
            row = next(ff)
            self.name, trade, price, quantity = row.split(",")
            min_price, max_price = float(price), float(price)
            for line in ff:
                name, trade, price, quantity = line.split(",")
                cost = float(price)
                if cost > max_price:
                    max_price = cost
                if cost < min_price:
                    min_price = cost
            half_sum = (min_price + max_price) / 2
            self.volatility = round(((max_price - min_price) / half_sum) * 100, 2)
            self.conn.send([self.name, self.volatility])
            self.conn.close()


@time_track
def main(path_ticker):
    files = generation_filename(path_file=path_ticker)
    parent_conn, child_conn = Pipe()
    pipes = []
    tickers = []
    tickers_data = {}
    for file in files:
        tickers.append(Ticker(file_name=file, conn=child_conn))
        pipes.append(parent_conn)
    for ticker in tickers:
        ticker.start()
    for conn in pipes:
        name, volatility = conn.recv()
        tickers_data[name] = volatility
    for ticker in tickers:
        ticker.join()
    sort_ticker(ticker_volatility=tickers_data)


path = Path.cwd()/"trades"
if __name__ == '__main__':
    main(path_ticker=path)
