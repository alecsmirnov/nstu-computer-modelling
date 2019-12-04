from math import sqrt, exp
from random import uniform
from scipy.stats import rayleigh, norm


# Метод суммирования (Вспомогательное распределение)
def summation_method(n):
    return (sum(uniform(0, 1) for _ in range(n)) - n / 2) / sqrt(n / 12)


# Поправка 2 для метода суммирования
def correction2(n):
    xi = summation_method(n)
    return xi - 41 * (xi**5 - 10 * xi**3 + 15 * xi) / (13440 * n**2)


# Нормальное распределение
def normal_distribution(n):
    return correction2(n)


# Распределения Рэлея (Основное распределение)
def rayleigh_distribution(_, sigm, n):
    return sigm * sqrt(normal_distribution(n)**2 + normal_distribution(n)**2)