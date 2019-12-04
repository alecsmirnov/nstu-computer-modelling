from math import sqrt
from random import uniform
from scipy.stats import f, chi2, norm


# Метод суммирования (Вспомогательное распределение)
def summation_method(n):
    return (sum(uniform(0, 1) for _ in range(n)) - n / 2) / sqrt(n / 12)


# Поправка 1 для метода суммирования
def correction1(n):
    eps = summation_method(n)
    return eps + (eps**3 - 3 * eps) / (20 * n)


# Нормальное распределение
def normal_distribution(n):
    return correction1(n)


# Распределение Хи-квадрат
def chi2_distribution(k, n):
    return sum(normal_distribution(n)**2 for _ in range(k))


# Распределения Фишера (Основное распределение)
def fisher_distribution(mu, nu, n):
    return chi2_distribution(mu, n) * nu / (chi2_distribution(nu, n) * mu)