# -*- coding: utf-8 -*-
# python3

from hashlib import sha1, sha256, sha512, md5, sha3_256
from time import time
from math import ceil
from numpy import linspace
import matplotlib.pyplot as plt


# numpy, matplotlib отсутствуют в стандартной библиотеке python3, их можно установить с помощью pip


def calc_hash(func, length):  # время вычисления хеш-функции func с аргументом длины length
    start_time = time()
    exec("{}(('a' * int({})).encode('utf-8'))".format(func, length))
    return time() - start_time


def delta(f, i, n_rounds=75):  # медиана изменения времени вычисления свёртки функции f, delta = 1
    return sorted([-f(i - j - 1) + f(i - j) for j in range(n_rounds)])[ceil(n_rounds / 2)]


# график медиан времени выполнения хеш-функций аналогичен графику хеш-функций, вычисленных 1 раз
def median(f, i, n_rounds=75):  # медиана значений функции f, вычисляемой n_rounds раз
    return [f(i) for _ in range(n_rounds)][ceil(n_rounds / 2)]


# график ср. арифм. времени выполнения хеш-функций аналогичен графику хеш-функций, вычисленных 1 раз
def average(f, i, n_rounds=75):  # среднее арифметическое значений функции f, вычисляемой n_rounds раз
    return sum([f(i) for _ in range(n_rounds)]) / n_rounds


def graph(func, l, color, title):  # func: название хеш-функции, l: множество аргументов, color: цвет линии
    # title: имя, отображаемое в легенде
    t = [calc_hash(func, i) for i in l]
    plt.plot(l, t, c=color, label=title)


def main():
    l = linspace(0, 500000000, 50)  # аргументы
    data = (("md5", "c", "MD5"), ("sha1", "r", "SHA-1"), ("sha256", "b", "SHA-256"), ("sha512", "g", "SHA-512"),
            ("sha3_256", "y", "SHA-3/256"))  # параметры отображения
    for h in data:
        graph(h[0], l, h[1], h[2])
    plt.title("график зависимости времени вычисления некоторых хеш-функций от длины входного массива", size=16)
    plt.xlabel("длина сообщения, байт", size=13)
    plt.ylabel("время вычисления, с", size=13)
    plt.grid()
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
