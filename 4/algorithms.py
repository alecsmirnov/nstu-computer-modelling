import math
import random
import scipy
import scipy.stats as stats
import scipy.integrate as integrate
import file_functions as ff


def rayleigh_density(x, sigm):
    return x / sigm**2 * scipy.exp(-x**2 / (2 * sigm**2))


def rayleigh_distribution(x, sigm):
    return 1 - scipy.exp(-x**2 / (2 * sigm**2))


def rayleigh_inverse(y, sigm):
    return sigm * math.sqrt(-2 * scipy.log(1 - y))


def make_sequence(n, sigm):
    return [rayleigh_inverse(random.uniform(0, 1), sigm) for _ in range(n)]


def get_intervals(sequence):
    k = int(5 * scipy.log10(len(sequence)))
    interval_width = max(sequence) / k
    intervals = [x * interval_width for x in range(0, k + 1)] 
    return intervals


def interval_hits(sequence, intervals):
    hits = [] 
    v = []
    for a, b in zip(intervals[:-1], intervals[1:]):
        hit = sum([a <= elem < b for elem in sequence])
        hits.append(hit)
        v.append(hit / len(sequence))
    return hits, v


def make_histogram(picturename, intervals, v, sigm):
    theor_intervals = []
    theor_v = []
    bar_width = intervals[-1] / (len(intervals) - 1)
    for i in range(len(intervals)):
        theor_intervals.append(i * bar_width + bar_width / 2)
        theor_v.append(rayleigh_distribution((i + 1) * bar_width, sigm) - rayleigh_distribution(i * bar_width, sigm))
    ff.draw_histogram(picturename, intervals, v, theor_intervals, theor_v, bar_width)


def chi2_test(sequence, intervals, hits, sigm, alpha):
    n = len(sequence)
    intervals_p = [rayleigh_distribution(x, sigm) - rayleigh_distribution(y, sigm) 
                   for x, y in zip(intervals[1:], intervals[:-1])]
    S = n * sum((hit / n - p)**2 / p if p else 0 for hit, p in zip(hits, intervals_p))
    r = len(intervals) - 1
    integral_res = integrate.quad(lambda S: S**(r / 2 - 1) * math.exp(-S / 2), S, math.inf)[0]
    PSS = integral_res / (2**(r / 2) * math.gamma(r / 2))
    PSS_passed = alpha < PSS
    return S, PSS, PSS_passed


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
        C1 = math.gamma(i + 0.5) * (4 * i + 1) / (math.gamma(0.5) * math.gamma(i + 1)) * (-1)**i
        C2 = math.exp(-(4 * i + 1)**2 * math.pi**2 / (8 * S)) 
        integral_res = integrate.quad(lambda y: math.exp(S / (8 * (y**2 + 1)) - 
                       ((4 * i + 1)**2 * math.pi**2 * y**2) / (8 * S)), 0, math.inf)[0] 
        result += C1 * C2 * integral_res
    result *= math.sqrt(2 * math.pi) / S 
    return result 


def anderson_darling_test(sequence, sigm, alpha):
    sort_sequence = sorted(sequence)
    S = 0 
    n = len(sort_sequence) 
    for i in range(1, n): 
        arg = (2 * i - 1) / (2 * n) 
        Fi = F(rayleigh_distribution(sort_sequence[i], sigm), 1) 
        S += arg * math.log(Fi) + (1 - arg) * math.log(1 - Fi)
    S = -n - 2 * S
    PSS = 1 - a2(S) 
    PSS_passed = alpha < PSS
    return S, PSS, PSS_passed