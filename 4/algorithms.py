from math import sqrt, exp, inf, gamma, pi
from scipy import log, log10
from scipy.integrate import quad
from random import uniform
from time import time
from file_functions import draw_histogram, draw_chart


# Функция плотности распределения Рэлея
def rayleigh_density(x, sigm):
    return x / sigm**2 * exp(-x**2 / (2 * sigm**2))


# Функция распределения Рэлея
def rayleigh_distribution(x, sigm):
    return 1 - exp(-x**2 / (2 * sigm**2))


# Обратная функция Рэлея
def rayleigh_inverse(y, sigm):
    return sigm * sqrt(-2 * log(1 - y))


# Генерация последовательности и подсчёт времени
def make_sequence(n, sigm):
    start_time = time()
    return [rayleigh_inverse(uniform(0, 1), sigm) for _ in range(n)], time() - start_time


# Разбиение последовательности на интервалы
def get_intervals(sequence):
    k = int(5 * log10(len(sequence)))
    interval_width = max(sequence) / k
    intervals = [x * interval_width for x in range(0, k + 1)] 
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
def make_histogram(picturename, intervals, v, sigm):
    theor_intervals = []
    theor_v = []
    bar_width = intervals[-1] / (len(intervals) - 1)
    for i in range(len(intervals)):
        theor_intervals.append(i * bar_width + bar_width / 2)
        theor_v.append(rayleigh_distribution((i + 1) * bar_width, sigm) - rayleigh_distribution(i * bar_width, sigm))
    draw_histogram(picturename, intervals, v, theor_intervals, theor_v, bar_width)


# Сформировать график функции
def make_charts(density_name, distribution_name, *arg):
    draw_chart(density_name, "Функция плотности распределения", "x", "f(x)", rayleigh_density, *arg)
    draw_chart(distribution_name, "Функция распределения", "x", "F(x)", rayleigh_distribution, *arg)


# Тест критерия типа Хи-квадрат
def chi2_test(sequence, intervals, hits, sigm, alpha):
    n = len(sequence)
    intervals_p = [rayleigh_distribution(x, sigm) - rayleigh_distribution(y, sigm) 
                   for x, y in zip(intervals[1:], intervals[:-1])]
    S = n * sum((hit / n - p)**2 / p if p else 0 for hit, p in zip(hits, intervals_p))
    r = len(intervals) - 1
    integral_res = quad(lambda S: S**(r / 2 - 1) * exp(-S / 2), S, inf)[0]
    PSS = integral_res / (2**(r / 2) * gamma(r / 2))
    passed = alpha < PSS
    return r, S, PSS, passed


def F(x, tetta):
    result = x / tetta
    if x < 0:
        result = 0
    elif tetta <= x:
        result = 1
    return result


def a2(S):
    result = 0
    iters_count = 10
    for i in range(iters_count):
        C1 = gamma(i + 0.5) * (4 * i + 1) / (gamma(0.5) * gamma(i + 1)) * (-1)**i
        C2 = exp(-(4 * i + 1)**2 * pi**2 / (8 * S)) 
        integral_res = quad(lambda y: exp(S / (8 * (y**2 + 1)) - 
                       ((4 * i + 1)**2 * pi**2 * y**2) / (8 * S)), 0, inf)[0] 
        result += C1 * C2 * integral_res
    result *= sqrt(2 * pi) / S 
    return result 


# Тест критерия типа Омега-квадрат Андерса-Дарлинга
def anderson_darling_test(sequence, sigm, alpha):
    sort_sequence = sorted(sequence)
    S = 0 
    n = len(sort_sequence) 
    for i in range(1, n): 
        arg = (2 * i - 1) / (2 * n) 
        Fi = F(rayleigh_distribution(sort_sequence[i], sigm), 1) 
        S += arg * log(Fi) + (1 - arg) * log(1 - Fi)
    S = -n - 2 * S
    PSS = 1 - a2(S) 
    passed = alpha < PSS
    return S, PSS, passed