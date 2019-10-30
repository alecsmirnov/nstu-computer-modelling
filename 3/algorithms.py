import math
import random
import numpy as np
import sympy as sp
import collections as col
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import file_functions as ff

PRECISION = 3


def draw_histogram(picturename, intervals, v, theor_intervals, theor_v):
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(theor_intervals, theor_v)
    plt.bar(intervals, v, width=1, align="edge", color="yellow")
    plt.xticks(np.arange(max(intervals) + 2))
    #title = ""
    #plt.title(title)
    #plt.xlabel("")
    #plt.ylabel("")
    plt.grid(True)
    plt.savefig(picturename)
    plt.clf()
    

def binomial_distribution(m, k, p):
    return sp.binomial(m, k) * p**k * (1 - p)**(m - k)


def r(n, k, p):
    return ((n - k) / (k + 1)) * (p / (1 - p))


def recurrence_formulas_alg(n, m, p):
    result = []
    operations_count = 8 + 4 * n
    P0 = binomial_distribution(m, 0, p)
    for _ in range(n):
        M = random.uniform(0, 1)
        k = 0
        P = P0
        while k < m and 0 <= M:
            M -= P
            k += 1
            P *= r(n, k, p)
            operations_count += 9
        result.append(k) 
    return result, operations_count, [P0]


def poisson_distribution(k, lambd):
    return math.exp(-lambd) * lambd**k / sp.factorial(k)


def poisson_alg(n, lambd):
    result = []
    L = int(lambd) 
    P = [poisson_distribution(i, L) for i in range(n)]
    Q = sum(P[:L + 1])
    operations_count = 4 + L + 9 * n
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
    return result, operations_count, P


def chi2_test(sequence, P, alpha, plot=False, output=True):
    n = len(sequence)
    implement_count = 0
    for i in range(len(P)):
        if n * P[i] <= 1:
            implement_count += 1
    interval_hits = col.Counter(sequence)
    v = []
    intervals = []
    for hit in interval_hits:
        v.append(interval_hits[hit] / n)
        intervals.append(hit)
    S = n * sum((interval_hits[i] / n - P[i])**2 / P[i] for i in range(implement_count))
    r = implement_count - 1
    integral_res = integrate.quad(lambda S: S**(r / 2 - 1) * math.exp(-S / 2), S, math.inf)[0]
    S_alpha = integral_res / (2**(r / 2) * math.gamma(r / 2))
    passed = alpha < S_alpha
    if plot == True:
        theor_intervals = [i for i in range(max(intervals) + 1)] 
        theor_v = P[:max(intervals) + 1]
        draw_histogram("chi2_test_histogram.png", intervals, v, theor_intervals, theor_v)
    if output == True:
        ff.write_chi2_results("chi2_test_result.txt", PRECISION, sequence, P, alpha, n, 0,0,0, v, 
                              S_alpha, implement_count, interval_hits, passed)
    return passed