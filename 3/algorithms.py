import math
import random
import sympy as sp
import collections as col
import scipy.integrate as integrate
import file_functions as ff


# Биномиальный закон распределения
def binomial_distribution(m, k, p):
    return sp.binomial(m, k) * p**k * (1 - p)**(m - k)


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
        M = random.uniform(0, 1)
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
    return math.exp(-lambd) * lambd**k / sp.factorial(k)


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
        M = random.uniform(0, 1) - Q
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
    interval_hits = col.Counter(sequence)
    n = len(sequence)
    for hit in interval_hits:
        v.append(interval_hits[hit] / n)
        intervals.append(hit)
    # Расчёт значения статистики критерия хи-квадрат
    S = n * sum((interval_hits[i] / n - P[i])**2 / P[i] for i in range(m + 1))
    r = m - 1
    integral_res = integrate.quad(lambda S: S**(r / 2 - 1) * math.exp(-S / 2), S, math.inf)[0]
    S_alpha = integral_res / (2**(r / 2) * math.gamma(r / 2))
    passed = alpha < S_alpha
    if plot == True:
        theor_intervals = [i for i in range(max(intervals) + 1)] 
        theor_v = P[:max(intervals) + 1]
        ff.draw_histogram(plot_name, intervals, v, theor_intervals, theor_v)
    return S, S_alpha, v, interval_hits, passed