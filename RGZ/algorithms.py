import random
import math
import mpmath
import time
import scipy
import scipy.stats as stats
import scipy.integrate as integrate

from mpmath import nsum, gamma, inf


def muller_method():
    p1, p2 = random.uniform(0, 1), random.uniform(0, 1)
    eps1 = math.sqrt(-2 * math.log(p1)) * math.cos(2 * math.pi * p2)
    eps2 = math.sqrt(-2 * math.log(p2)) * math.sin(2 * math.pi * p1)
    return eps1, eps2


def chi2_distribution(k):
    return sum(val**2 for sub in (muller_method() for _ in range(k)) for val in sub)


def fisher_distribution(mu, nu):
    return chi2_distribution(mu) * nu / (chi2_distribution(nu) * mu)


def make_sequence(n, mu, nu):
    start_time = time.time()
    sequence = [fisher_distribution(mu, nu) for _ in range(n)]
    modeling_time = time.time() - start_time
    return sequence, modeling_time


# Разбиение последовательности на интервалы
def get_intervals(sequence):
    k = int(5 * scipy.log10(len(sequence)))
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


# Тест критерия Хи-квадрат
def chi2_test(sequence, intervals, hits, mu, nu, alpha):
    n = len(sequence)
    intervals_p = [stats.f.cdf(x, mu, nu) - stats.f.cdf(y, mu, nu) 
                   for x, y in zip(intervals[1:], intervals[:-1])]
    S = n * sum((hit / n - p)**2 / p if p else 0 for hit, p in zip(hits, intervals_p))
    r = len(intervals) - 1
    integral_res = integrate.quad(lambda S: S**(r / 2 - 1) * math.exp(-S / 2), S, math.inf)[0]
    PSS = integral_res / (2**(r / 2) * math.gamma(r / 2))
    passed = alpha < PSS
    return r, S, PSS, passed


def F(sequence, i):
    return sum(1 for x in sorted(sequence) if x < i) / len(sequence)


def I(mu, z):
    return float(nsum(lambda i: (z / 2)**(mu + 2 * i) / (gamma(i + 1) * gamma(i + mu + 1)), [0, inf]))


def a1(S):
    def sum_item(i):
        z = (4 * i + 1)**2 / (16 * S)
        val1 = gamma(i + 0.5) * math.sqrt(4 * i + 1) / (gamma(0.5) * gamma(i + 1)) * math.exp(-z)
        val2 = I(-0.25, z) - I(0.25, z)
        return val1 * (val2 - int(val2))
    ITER_MAX = 5
    result = float(nsum(sum_item, [0, ITER_MAX])) / math.sqrt(2 * S)
    return result 


def cms_test(sequence, mu, nu, alpha):
    sort_sequence = sorted(sequence)
    n = len(sort_sequence)
    S = 1 / (12 * n) + sum((F(stats.f.cdf(sort_sequence[i], mu, nu), i) - (2 * i - 1) / (2 * n))**2 for i in range(n))
    PSS = 1 - a1(S) 
    passed = alpha < PSS
    return S, PSS, passed