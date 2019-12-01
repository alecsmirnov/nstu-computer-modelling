import file_functions as ff
from math import sqrt, gamma, log, log10, exp, cos, sin, pi
from mpmath import nsum, inf
from scipy.stats import f
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
    return sum(val**2 for sub in (muller_method() for _ in range(k)) for val in sub)


# Распределения Фишера
def fisher_distribution(mu, nu):
    return chi2_distribution(mu) * nu / (chi2_distribution(nu) * mu)


# Генерация последовательности и подсчёт времени
def make_sequence(n, mu, nu):
    start_time = time()
    sequence = [fisher_distribution(mu, nu) for _ in range(n)]
    modeling_time = time() - start_time
    return sequence, modeling_time


# Разбиение последовательности на интервалы
def get_intervals(sequence):
    k = int(5 * log10(len(sequence)))
    intervals_width = max(sequence) / k
    intervals = [x * intervals_width for x in range(0, k + 1)] 
    return intervals


# Расчёт попаданий элементов последовательности в интервалы
def interval_hits(sequence, intervals):
    hits = [] 
    v = []
    for a, b in zip(intervals[:-1], intervals[1:]):
        hit = sum([a <= elem < b for elem in sequence])
        hits.append(hit)
        v.append(hit / len(sequence))
    return hits, v


# Сформировать гистограмму теоретической и эмпирической функции плотности распределения
def make_histogram(picturename, intervals, v, mu, nu):
    theor_intervals = []
    theor_v = []
    bar_width = intervals[-1] / (len(intervals) - 1)
    for i in range(len(intervals)):
        theor_intervals.append(i * bar_width + bar_width / 2)
        theor_v.append(f.cdf((i + 1) * bar_width, mu, nu) - f.cdf(i * bar_width, mu, nu))
    ff.draw_histogram(picturename, intervals, v, theor_intervals, theor_v, bar_width)


# Сформировать график функции
def make_chart(picturename, mu, nu):
    ff.draw_chart(picturename, "Функция распределения Фишера", "x", "F(x)", f.cdf, mu, nu)


# Тест критерия Хи-квадрат
def chi2_test(sequence, intervals, hits, mu, nu, alpha):
    n = len(sequence)
    intervals_p = [f.cdf(x, mu, nu) - f.cdf(y, mu, nu) for x, y in zip(intervals[1:], intervals[:-1])]
    S = n * sum((hit / n - p)**2 / p if p else 0 for hit, p in zip(hits, intervals_p))
    r = len(intervals) - 1
    integral_res = quad(lambda S: S**(r / 2 - 1) * exp(-S / 2), S, inf)[0]
    PSS = integral_res / (2**(r / 2) * gamma(r / 2))
    passed = alpha < PSS
    return r, S, PSS, passed


# Подсчёт кол-ва реализации случайной величины
def F(sequence, i):
    return sum(1 for x in sorted(sequence) if x < i) / len(sequence)


def I(mu, z):
    return float(nsum(lambda i: (z / 2)**(mu + 2 * i) / (gamma(i + 1) * gamma(i + mu + 1)), [0, inf]))


def a1(S):
    def sum_item(i):
        z = (4 * i + 1)**2 / (16 * S)
        val1 = gamma(i + 0.5) * sqrt(4 * i + 1) / (gamma(0.5) * gamma(i + 1)) * exp(-z)
        val2 = I(-0.25, z) - I(0.25, z)
        return val1 * (val2 - int(val2))
    ITER_MAX = 5
    result = float(nsum(sum_item, [0, ITER_MAX])) / sqrt(2 * S)
    return result 


# Тест критерия Крамера-Мизеса-Смирнов
def cms_test(sequence, mu, nu, alpha):
    sorted_seq = sorted(sequence)
    n = len(sorted_seq)
    S = 1 / (12 * n) + sum((F(f.cdf(sorted_seq[i], mu, nu), i) - (2 * i - 1) / (2 * n))**2 for i in range(n))
    PSS = 1 - a1(S) 
    passed = alpha < PSS
    return S, PSS, passed