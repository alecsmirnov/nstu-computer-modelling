import file_functions as ff
from math import sqrt, gamma, log, log10, exp, cos, sin, pi
from mpmath import nsum, inf
from scipy.stats import f, chi2
from scipy.integrate import quad
from random import uniform
from time import time


# Метод моделирования вспомогательного распределения
def muller_method():
    p1, p2 = uniform(0, 1), uniform(0, 1)
    eps1 = sqrt(-2 * log(p1)) * cos(2 * pi * p2)
    eps2 = sqrt(-2 * log(p2)) * sin(2 * pi * p1)
    return eps1, eps2


# Распределение Хи-квадрат
def chi2_distribution(k):
    return sum(val**2 for sub in (muller_method() for _ in range(k // 2)) for val in sub)


# Распределения Фишера (Основное распределение)
def fisher_distribution(mu, nu):
    return chi2_distribution(mu) * nu / (chi2_distribution(nu) * mu)


# Генерация последовательности и подсчёт времени
def make_sequence(n, distribution, *args):
    start_time = time()
    sequence = [distribution(*args) for _ in range(n)]
    modeling_time = time() - start_time
    return sequence, modeling_time


# Разбиение последовательности на интервалы и расчёт ширины интервалов
def get_intervals(sequence):
    k = int(5 * log10(len(sequence)))
    intervals_width = (max(sequence) - min(sequence)) / k
    intervals = [x * intervals_width + min(sequence) for x in range(0, k + 1)] 
    return intervals, intervals_width


# Расчёт (вероятностей) попаданий элементов последовательности в интервалы
def interval_hits(sequence, intervals):
    hits = [] 
    v = []
    for a, b in zip(intervals[:-1], intervals[1:]):
        hit = sum([a <= elem < b for elem in sequence])
        hits.append(hit)
        v.append(hit / len(sequence))
    return hits, v


# Сформировать гистограмму теоретической и эмпирической функции плотности распределения
def make_histogram(picturename, title, intervals, intervals_width, v, theor_distributuon, *args):
    theor_intervals = [x + intervals_width / 2 for x in intervals]
    theor_v = [theor_distributuon(x, *args) - theor_distributuon(y, *args) 
               for x, y in zip(intervals[1:], intervals[:-1])]
    ff.draw_histogram(picturename, title, intervals, v, theor_intervals, theor_v, intervals_width)


# Сформировать график функции
def make_chart(picturename, title, theor_distributuon, *args):
    ff.draw_chart(picturename, title, "x", "F(x)", theor_distributuon, *args)


# Тест критерия Хи-квадрат
def chi2_test(n, intervals, hits, alpha, theor_distributuon, *args):
    intervals_p = [theor_distributuon(x, *args) - theor_distributuon(y, *args) 
                   for x, y in zip(intervals[1:], intervals[:-1])]
    S = n * sum((hit / n - p)**2 / p if p else 0 for hit, p in zip(hits, intervals_p))
    r = len(intervals) - 1
    integral_res = quad(lambda S: S**(r / 2 - 1) * exp(-S / 2), S, inf)[0]
    PSS = integral_res / (2**(r / 2) * gamma(r / 2))
    passed = alpha < PSS
    return r, S, PSS, passed


def I(mu, z):
    return float(nsum(lambda i: (z / 2)**(mu + 2 * i) / (gamma(i + 1) * gamma(i + mu + 1)), [0, inf]))


def a1(S):
    def sum_item(i):
        z = (4 * i + 1)**2 / (16 * S)
        val1 = gamma(i + 0.5) * sqrt(4 * i + 1) / (gamma(0.5) * gamma(i + 1)) * exp(-z)
        val2 = I(-0.25, z) - I(0.25, z)
        return val1 * val2
    ITER_MAX = 5
    result = float(nsum(sum_item, [0, ITER_MAX])) / sqrt(2 * S)
    return result 


# Тест критерия Крамера-Мизеса-Смирнов
def cms_test(sequence, alpha, theor_distributuon, *args):
    sorted_seq = sorted(sequence)
    n = len(sorted_seq)
    S = 1 / (12 * n) + sum((theor_distributuon(sorted_seq[i], *args) - (2 * i - 1) / (2 * n))**2 for i in range(n))
    PSS = 1 - a1(S) 
    passed = alpha < PSS
    return S, PSS, passed