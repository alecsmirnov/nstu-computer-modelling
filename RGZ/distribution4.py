from math import sqrt, log, cos, sin, pi
from random import uniform
from scipy.stats import t, chi2, norm


# Метод Мюллера (Вспомогательное распределение)
def muller_method():
    p1, p2 = uniform(0, 1), uniform(0, 1)
    xi1 = sqrt(-2 * log(p1)) * cos(2 * pi * p2)
    xi2 = sqrt(-2 * log(p2)) * sin(2 * pi * p1)
    return xi1, xi2


# Нормальное распределение
def normal_distribution(even=[True], xi=[0.0, 0.0]):
    if even[0] == True:
        xi[0], xi[1] = muller_method()
    else:
        xi[0] = xi[1]
    even[0] = not even[0]
    return xi[0]


# Распределение Хи-квадрат
def chi2_distribution(k):
    return sum(normal_distribution()**2 for _ in range(k))


# Распределение Стьюдента
def student_distribution(n):
    return sqrt(n) * normal_distribution() / sqrt(chi2_distribution(n))