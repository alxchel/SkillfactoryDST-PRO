import numpy as np


def score_game(game_core):
    """Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число"""
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1, 101, size=(1000))
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return (score)


def game_core_v3(number):
    """Ищет заданное число методом деления пополам.
       Функция принимает загаданное число и возвращает число попыток"""
    lower, upper = 1, 100  # диапазон для поиска, включительно
    count = 0
    while True:
        count += 1
        predict = (lower + upper) // 2  # проверяем в центре
        if predict == number:  # выход из цикла, если угадали
            break
        if lower == upper:
            raise Exception('Загадано число вне диапазона!')
        if number > predict:
            lower = predict + 1  # значение в верхней половине
        else:
            upper = predict - 1  # значение в нижней половине
    return count


# Проверяем
score_game(game_core_v3)
