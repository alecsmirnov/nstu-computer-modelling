import random
import math

import sys
import numpy as np
import matplotlib.pyplot as plt

import scipy
import scipy.stats as stats
import scipy.integrate as integrate


def draw_chart(picturename, title, x_label, y_label, func, *arg):
    X_MAX = 10
    X_STEP = 0.005
    x = np.arange(0, X_MAX + X_STEP, X_STEP) 
    plt.xticks(range(0, X_MAX + 1))
    plt.title(title)
    plt.xlabel(x_label) 
    plt.ylabel(y_label)
    y = [func(x, *arg) for x in x]
    plt.plot(x, y)
    plt.grid(True)
    plt.savefig(picturename)
    plt.clf()


def muller_method():
    p1, p2 = random.uniform(0, 1), random.uniform(0, 1)
    eps1 = math.sqrt(-2 * math.log(p1)) * math.cos(2 * math.pi * p2)
    eps2 = math.sqrt(-2 * math.log(p2)) * math.sin(2 * math.pi * p1)
    return eps1, eps2


def chi2_distribution(k):
    return sum(val**2 for sub in (muller_method() for _ in range(k)) for val in sub)


def fisher_distribution(mu, nu):
    return chi2_distribution(mu) * nu / (chi2_distribution(nu) * mu)


def generate_sequence(n, mu, nu):
    return [fisher_distribution(mu, nu) for _ in range(n)]


# Разбиение последовательности на интервалы
def get_intervals(sequence):
    k = int(5 * scipy.log10(len(sequence)))
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


def draw_histogram(picturename, intervals, v, theor_intervals, theor_v, bar_width):
    plt.xlabel("Интервалы")
    plt.ylabel("Частоты")
    plt.xticks(intervals, rotation=90)
    plt.plot(theor_intervals, theor_v, marker="o")
    plt.bar(intervals[:len(intervals) - 1], v, width=bar_width, alpha=0.5, 
            align="edge", edgecolor="grey", color="lightgrey")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(picturename)
    plt.clf()


# Сформировать гистограмму теоретической и эмпирической функции плотности распределения
def make_histogram(picturename, intervals, v, mu, nu):
    theor_intervals = []
    theor_v = []
    bar_width = intervals[-1] / (len(intervals) - 1)
    for i in range(len(intervals)):
        theor_intervals.append(i * bar_width + bar_width / 2)
        theor_v.append(stats.f.cdf((i + 1) * bar_width, mu, nu) - stats.f.cdf(i * bar_width, mu, nu))
    draw_histogram(picturename, intervals, v, theor_intervals, theor_v, bar_width)


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


def main():
    alpha = 0.05
    n = 50
    mu = 4
    nu = 2
    sequence = generate_sequence(n, mu, nu)
    intervals = get_intervals(sequence)
    hits, v = interval_hits(sequence, intervals)
    make_histogram("hist.png", intervals, v, mu, nu)
    r, S, PSS, passed = chi2_test(sequence, intervals, hits, mu, nu, alpha)
    print(r)
    print(S)
    print(PSS)
    print(passed)


if __name__ == "__main__":
    main()