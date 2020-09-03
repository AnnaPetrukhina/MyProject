import time
from operator import itemgetter
import os


def sort_ticker(ticker_volatility):
    tickers_nil = []
    tickers_data_sort = sorted(ticker_volatility.items(), key=itemgetter(1))
    index_nil = 0
    for tick in tickers_data_sort:
        if tick[1] == 0:
            tickers_nil.append(tick[0])
        else:
            index_nil = tickers_data_sort.index(tick)
            break
    for i in range(1, 4):
        print(tickers_data_sort[-i][0], tickers_data_sort[-i][1])
    for i in range(index_nil + 2, index_nil - 1, -1):
        print(tickers_data_sort[i][0], tickers_data_sort[i][1])
    print("\nНулевая волатильность:")
    for tick in sorted(tickers_nil):
        print(f"{tick}", end=" ")


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'\n\nФункция работала {elapsed} секунд(ы)')
        return result
    return surrogate

def generation_filename(path_file):
    for dirpath, dirnames, filenames in os.walk(path_file):
        for f in filenames:
            file_path = os.path.join(dirpath, f)
            yield file_path
