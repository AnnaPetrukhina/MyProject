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
from multiprocessing import Process, Queue
from sort import sort_ticker, time_track, generation_filename


class Ticker(Process):

    def __init__(self, file_name, collector,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = file_name
        self.volatility = 0
        self.name = ""
        self.collector = collector

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
            self.collector.put((self.name, self.volatility))


@time_track
def main(path_ticker):
    files = generation_filename(path_file=path_ticker)
    collector = Queue()
    tickers_data = {}
    tickers = [Ticker(file_name=file, collector=collector) for file in files]
    for ticker in tickers:
        ticker.start()
    for ticker in tickers:
        ticker.join()
    while not collector.empty():
        data = collector.get()
        ticker_name = data[0]
        ticker_volatility = data[1]
        tickers_data[ticker_name] = ticker_volatility
    sort_ticker(ticker_volatility=tickers_data)


path = Path.cwd()/"trades"
if __name__ == '__main__':
    main(path_ticker=path)
