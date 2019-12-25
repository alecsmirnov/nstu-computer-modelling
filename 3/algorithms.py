from math import exp, inf, gamma
from scipy.stats import chi2
from sympy import binomial, factorial
from scipy.integrate import quad
from random import uniform
from collections import Counter
from file_functions import draw_histogram


# Биномиальный закон распределения
def binomial_distribution(m, k, p):
    return binomial(m, k) * p**k * (1 - p)**(m - k)


def r(m, k, p):
    return ((m - k) / (k + 1)) * (p / (1 - p))


# Стандартный алгоритм с рекуррентными формулами
def recurrence_formula(n, m, p):
    result = []
    # Количество операций
    operations_count = 8 + 4 * n
    # Вероятности случайной величины из m интервалов
    P = [binomial_distribution(m, i, p) for i in range(m + 1)]
    # Генерация чисел, принадлежащих распределению и попаданию в интервал из m
    for _ in range(n):
        M = uniform(0, 1)
        Pk = P[0]
        k = 0
        # Проверка попадания в интервал
        search = True
        while search:
            M -= Pk
            if M < 0:
                search = False
            else:
                Pk *= r(m, k, p)
                k += 1
            operations_count += 9
        result.append(k) 
    return result, operations_count, P, m


# Закон распределения Пуассона
def poisson_distribution(k, lambd):
    return exp(-lambd) * lambd**k / factorial(k)


# Нестандартный алгоритм для распределения Пуассона
def poisson(n, lambd):
    result = []
    # Параметр рапсределения Пуассона
    L = int(lambd) 
    # Вероятности случайной величины из n интервалов
    P = [poisson_distribution(i, L) for i in range(n)]
    # Количество возможных реализаций моделируемой величины
    m = 0
    for i in range(len(P)):
        #if n * P[i] <= 1:
        if 100 * P[i] <= 1:
            m += 1
    Q = sum(P[:L + 1])
    operations_count = 4 + L + 9 * n
    # Генерация чисел, принадлежащих распределению и попаданию в интервал из n
    for _ in range(n):
        M = uniform(0, 1) - Q
        k = L
        if 0 <= M: 
            while 0 <= M:
                k += 1
                M -= P[k]
                operations_count += 2
        else:
            k += 1
            operations_count += 1
            while M < 0:
                k -= 1
                M += P[k]
                operations_count += 2
        result.append(k)
    return result, operations_count, P, m


# Тест критерия типа хи-квадрат
def chi2_test(sequence, P, m, alpha, plot=False, plot_name="chi2_test_histogram.png"):
    # Относительные частоты попадания в интервал
    v = []
    intervals = []
    interval_hits = Counter(sequence)
    n = len(sequence)
    for hit in interval_hits:
        v.append(interval_hits[hit] / n)
        intervals.append(hit)
    # Расчёт значения статистики критерия хи-квадрат
    S = n * sum((interval_hits[i] / n - P[i])**2 / P[i] for i in range(m + 1))
    r = m - 1
    integral_res = quad(lambda S: S**(r / 2 - 1) * exp(-S / 2), S, inf)[0]
    PSS = integral_res / (2**(r / 2) * gamma(r / 2))
    PSS_passed = alpha < PSS
    S_alpha = chi2.isf(alpha, r)
    S_alpha_passed = S < S_alpha
    if plot:
        theor_intervals = [i for i in range(max(intervals) + 1)] 
        theor_v = P[:max(intervals) + 1]
        draw_histogram(plot_name, intervals, v, theor_intervals, theor_v)
    return S, S_alpha, PSS, v, interval_hits, S_alpha_passed, PSS_passed