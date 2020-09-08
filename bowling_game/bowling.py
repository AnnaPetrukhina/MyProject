import logging


class GetFrame:

    def __init__(self, game_result):
        self.result = game_result

    def __iter__(self):
        self.i = 0
        return self

    def _count_frame(self):
        strike = ["X", "Х"]
        count_strike = 0
        if strike[0] in self.result or strike[1] in self.result:
            count_strike = self.result.count(strike[0])
            count_strike += self.result.count(strike[1])
        count_without_strike = 10 - count_strike
        length_without_strike = count_without_strike * 2
        if length_without_strike != len(self.result) - count_strike:
            raise IndexError(f"Введен некорректный результат {self.result}")

    def _symbol_in_frame(self):
        numeral = [str(x) for x in list(range(1, 10))]
        symbols = ["X", "Х", "-", "/"]
        symbols.extend(numeral)
        expected_symbols = set(symbols)
        received_symbols = set(self.result)
        if received_symbols.difference(expected_symbols):
            raise ValueError(f"Введен некорректный символ в результате {self.result}. Результат не может содержать"
                             f" символы {received_symbols.difference(expected_symbols)}")

    def __next__(self):
        numeral = [str(x) for x in list(range(1, 10))]
        self._count_frame()
        self._symbol_in_frame()
        while self.i < len(self.result):
            symbol_1 = self.result[self.i]
            if symbol_1 == "Х" or symbol_1 == "X":
                frame = [symbol_1]
            elif symbol_1 == "/":
                raise ValueError(f"Введен некорректный результат. Фрейм не может начинаться с {symbol_1}")
            else:
                self.i += 1
                symbol_2 = self.result[self.i]
                if symbol_2 == "Х" or symbol_2 == "X":
                    raise ValueError(f"{symbol_2} не может быть на второй позиции в фрейме. "
                                     f"Введен некорректный фрейм {symbol_1 + symbol_2}.")
                elif symbol_1 in numeral and symbol_2 in numeral:
                    if int(symbol_1) + int(symbol_2) >= 10:
                        raise ValueError(f"Введен некорректный фрейм {symbol_1 + symbol_2} в результате {self.result}.")
                frame = [symbol_1, symbol_2]
            logging.debug(f' фрейм {frame}')
            self.i += 1
            return frame
        raise StopIteration()


class GetScore:

    def __init__(self, game_result):
        self.result = game_result
        self.score = 0

    def strike(self, frame):
        logging.debug(f' {frame} страйк - 20 очков')
        self.score += 20

    def spare(self, frame):
        logging.debug(f' {frame} spare - 15 очков')
        self.score += 15

    def sum_frame(self, frame):
        sum_f = int(frame[0]) + int(frame[1])
        logging.debug(f' {frame} - {sum_f}')
        self.score += sum_f

    def emptiness(self, frame):
        if frame[0] == frame[1]:
            logging.debug(f' {frame} - 0 очков')
            self.score += 0
        elif frame[0] == "-":
            logging.debug(f' {frame} - {frame[1]} очков')
            self.score += int(frame[1])
        else:
            logging.debug(f' {frame} - {frame[0]} очков')
            self.score += int(frame[0])

    def run(self):
        strike = ["X", "Х"]
        frames = [x for x in GetFrame(self.result)]
        for frame in frames:
            f = "".join(frame)
            if f in strike:
                self.strike(f)
            elif "/" in f:
                self.spare(f)
            elif "-" in f:
                self.emptiness(frame=f)
            else:
                self.sum_frame(frame=f)
        logging.debug(f' {self.result} - {self.score} очков\n')
        return self.score


log = logging.getLogger('Bowling')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("errors_bowling.log", 'w', 'utf-8', delay=True)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M')
fh.setFormatter(formatter)
log.addHandler(fh)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    result_game = "Х4/34-49/1245--8/X"
    try:
        log.info(f'Посчитаем количество очков результата {result_game}')
        get_score = GetScore(result_game)
        score = get_score.run()
        log.info(f'{result_game} - {score}')
    except Exception as ex:
        log.exception(f'{ex}')
