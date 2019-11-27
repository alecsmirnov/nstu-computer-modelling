import math
import random
import time
import scipy
import scipy.stats as stats
import scipy.integrate as integrate
import file_functions as ff


# Функция плотности распределения Мояла
def moyal_density(x, mu, sigm):
    return 1 / (math.sqrt(2 * math.pi) * sigm) * math.exp((mu - x) / (2 * sigm) - math.exp((mu - x) / sigm) / 2)


# Функция распределения Мояла
def moyal_distribution(x, mu, sigm):
    return -math.erf(math.exp((mu - x) / (2 * sigm)) / math.sqrt(2))


def frange(x, y, jump):
  while x < y:
    yield x
    x += jump


# Метод исключений (Неймана)
def neumann_method(a, b, mu, sigm):
    max_density = max([moyal_density(x, mu, sigm) for x in frange(a, b, (b - a) / 100)])
    x0 = a + random.uniform(0, 1) * (b - a) 
    y0 = random.uniform(0, 1) * max_density
    n = 2 
    while moyal_density(x0, mu, sigm) <= y0: 
        n += 2
        x0 = a + random.uniform(0, 1) * (b - a)
        y0 = random.uniform(0, 1) * max_density
    return x0, n, max_density


# Генерация последовательности и подсчёт времени
def make_sequence(n, a, b, mu, sigm):
    start_time = time.time()
    sequence = []
    density = []
    count = 0
    for _ in range(n):
        x, n, max_density = neumann_method(a, b, mu, sigm)
        sequence.append(x)
        density.append(max_density)
        count += n
    modeling_time = time.time() - start_time
    return sequence, max(density), count, modeling_time


# Определить границы интервала
def get_bounds(mu, sigm):
    a = scipy.stats.norm.ppf(0.01, loc=mu, scale=sigm)
    b = scipy.stats.norm.ppf(0.99, loc=mu, scale=sigm)
    return a, b


# Разбиение последовательности на интервалы
def get_intervals(sequence):
    k = int(5 * scipy.log10(len(sequence)))
    intervals_width = (max(sequence) - min(sequence)) / k
    intervals = [x * intervals_width + min(sequence) for x in range(0, k + 1)] 
    return intervals, intervals_width


# Расчёт попаданий элементов последовательности в интервалы
def interval_hits(sequence, intervals):
    hits = [] 
    v = []
    for a, b in zip(intervals[:-1], intervals[1:]):
        hit = sum([a <= elem < b for elem in sequence])
        hits.append(hit)
        v.append(hit / len(sequence))
    return hits, v


# Сформировать гистограмму теоретической и эмпирической функции плотности распределения
def make_histogram(picturename, intervals, intervals_width, v, mu, sigm):
    theor_intervals = intervals[:len(intervals) - 1] + intervals_width / 2
    theor_v = [moyal_distribution(x, mu, sigm) - moyal_distribution(y, mu, sigm) for x, y in zip(intervals[1:], intervals[:-1])]
    ff.draw_histogram(picturename, intervals, v, theor_intervals, theor_v, intervals_width)


# Сформировать график функции
def make_charts(density_name, distribution_name, a, b, mu, sigm):
    ff.draw_chart(density_name, "Функция плотности распределения Мояла", "x", "f(x)", a, b, moyal_density, mu, sigm)
    ff.draw_chart(distribution_name, "Функция распределения Мояла", "x", "F(x)", a, b, moyal_distribution, mu, sigm)


# Тест критерия Хи-квадрат
def chi2_test(sequence, intervals, hits, mu, sigm, alpha):
    n = len(sequence)
    intervals_p = [moyal_distribution(x, mu, sigm) - moyal_distribution(y, mu, sigm) 
                   for x, y in zip(intervals[1:], intervals[:-1])]
    S = n * sum((hit / n - p)**2 / p if p else 0 for hit, p in zip(hits, intervals_p))
    r = len(intervals) - 1
    integral_res = integrate.quad(lambda S: S**(r / 2 - 1) * math.exp(-S / 2), S, math.inf)[0]
    PSS = integral_res / (2**(r / 2) * math.gamma(r / 2))
    passed = alpha < PSS
    return r, S, PSS, passed


# Разность между накопленными частотами
def calc_D(sequence, mu, sigm):
    n = len(sequence)
    D_plus = max([(i+1) / n - moyal_distribution(sequence[i], mu, sigm) for i in range(n)])
    D_minus = max([moyal_distribution(sequence[i], mu, sigm) - i / n for i in range(n)])
    return max(D_plus, D_minus)


# Тест критерия Смирнова
def smirnov_test(sequence, mu, sigm, alpha):
    sort_seq = sorted(sequence)
    n = len(sort_seq)
    S = (6 * n * calc_D(sort_seq, mu, sigm) + 1)**2 / (9 * n)
    PSS = math.exp(-S / 2)
    passed = alpha < PSS
    return S, PSS, passed