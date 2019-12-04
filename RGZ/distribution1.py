from math import sqrt, log, cos, sin, pi
from random import uniform
from scipy.stats import f, chi2, norm


# Метод Мюллера (Вспомогательное распределение)
def muller_method():
    p1, p2 = uniform(0, 1), uniform(0, 1)
    eps1 = sqrt(-2 * log(p1)) * cos(2 * pi * p2)
    eps2 = sqrt(-2 * log(p2)) * sin(2 * pi * p1)
    return eps1, eps2


# Нормальное распределение
def normal_distribution(even=[True], eps=[0.0, 0.0]):
    if even[0] == True:
        eps[0], eps[1] = muller_method()
    else:
        eps[0] = eps[1]
    even[0] = not even[0]
    return eps[0]


# Распределение Хи-квадрат
def chi2_distribution(k):
    return sum(normal_distribution()**2 for _ in range(k))


# Распределения Фишера (Основное распределение)
def fisher_distribution(mu, nu):
    return chi2_distribution(mu) * nu / (chi2_distribution(nu) * mu)