from random import sample


def think_number():
    global number
    number = ""
    numeral_str = list(range(10))
    number_list = sample(numeral_str, 4)
    while number_list[0] == 0:
        number_list = sample(numeral_str, 4)
    for numeral in number_list:
        number += str(numeral)
    return number


def check_number(guess):
    answer = {'bulls': 0, 'cows': 0}
    if guess == number:
        answer["bulls"] = 4
        answer["cows"] = 0
    else:
        for i, numeral in enumerate(guess):
            if number[i] == numeral:
                answer["bulls"] += 1
            elif numeral in number:
                answer["cows"] += 1
    return answer


number = ""
