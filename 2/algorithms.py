from math import sqrt, floor, log2, exp, gamma, inf
from mpmath import nsum
from scipy.stats import norm, chi2
from scipy.integrate import quad


# Генератор псевдослучайно последовательности
def generator(x0, a, b, c, n, m):
    x = [x0]
    for i in range(n - 1):
        x.append((a * x[i]**2 + b * x[i] + c) % m)
    return x


# Выделение периода последовательности с отбрасыванием предпериода
def period(sequence):
    # Инвертируем последовательность
    seq = list(reversed(sequence))
    # Проверяем подпоследовательности до середины последовательности
    max_len = len(seq) // 2 + 1
    # Увеличиваем длину подпоследовательности и проверяем на равенство соседнюю за ней
    for i in range(1, max_len):
        if seq[0:i] == seq[i:2*i]:
            return seq[0:i]
    return seq


# Тест проверки перестановок
def test1(x, _, alpha):
    n = len(x)
    # Квантиль нормального распределения уровня 1 - alpha / 2
    U = norm.ppf(1 - alpha / 2)
    # Количество перестановок
    Q = 0
    for i in range(n - 1): 
        if x[i] > x[i+1]:
            Q += 1
    # Доверительный интервал по смоделированной выборке оценке числа перестановок Q
    a = Q - U * sqrt(n) / 2
    b = Q + U * sqrt(n) / 2
    # Проверка попадания оценки в доверительный интервал
    passed = a <= n / 2 <= b
    return n, Q, a, b, passed


# Получить список относительных частот попадания в интервал
def calc_frequencies(x, m, K):
    n = len(x)
    # Количество попаданий в каждый интервал
    interval_hit = [0] * K
    for i in range(n):
        for j in range(K):
            if m / K * j <= x[i] < m / K * (j+1):
                interval_hit[j] += 1
    # Расчёт относительных частот попадания в интервал
    v = [x/n for x in interval_hit]
    return v


# Частотный тест
def frequencies_test(v, n, m, K, alpha):
    # Частоты, для которых доверительный интервал не содержит теоретическую частоту
    frequencies_table = []
    passed = True
    # Квантиль нормального распределения уровня 1 - alpha / 2
    U = norm.ppf(1 - alpha / 2)
    for i in range(K):
        # Построение доверительного интервала
        a = v[i] - U / K * sqrt((K - 1) / n) 
        b = v[i] + U / K * sqrt((K - 1) / n)
        # Проверка попадания частоты в доверительный интервал
        if not (a <= 1 / K <= b): 
            passed = False
        frequencies_table.append([i, a, b, v[i], a <= 1 / K <= b])
    return frequencies_table, passed


# Тест оценки сходимости математического ожидания
def MX_estimate_test(MX, DX, n, m, alpha):
    # Квантиль нормального распределения уровня 1 - alpha / 2
    U = norm.ppf(1 - alpha / 2)
    # Построение доверительного интервала
    a = MX - U * sqrt(DX) / sqrt(n)
    b = MX + U * sqrt(DX) / sqrt(n) 
    passed = a <= m / 2 <= b
    return a, b, m / 2, passed


# Тест оценки сходимости дисперсии
def DX_estimate_test(DX, n, m, alpha):
    # Построение доверительного интервала
    a = (n - 1) * DX / chi2.isf(alpha / 2, n - 1)
    b = (n - 1) * DX / chi2.isf(1 - alpha / 2, n - 1)
    passed = a <= m**2 / 12 <= b
    return a, b, m**2 / 12, passed


# Тест на равномерность 
def test2(x, m, K, alpha):
    MX = sum(x) / len(x)
    DX = sum([(x - MX)**2 for x in x]) / (len(x) - 1)
    # Получение относительных частот попадания в интервал
    v = calc_frequencies(x, m, K)
    n = len(x) 
    # Результаты частотного теста
    freq_table, freq_pass  = frequencies_test(v, n, m, K, alpha)
    # Результаты теста оценки сходимости математического ожидания
    MX_a, MX_b, MX_val, MX_pass = MX_estimate_test(MX, DX, n, m, alpha)
    # Результаты теста оценки сходимости дисперсии
    DX_a, DX_b, DX_val, DX_pass = DX_estimate_test(DX, n, m, alpha)
    passed = freq_pass and MX_pass and DX_pass
    return n, m, K, v, freq_table, freq_pass, MX, MX_a, MX_b, MX_val, MX_pass, DX, DX_a, DX_b, DX_val, DX_pass, passed


# Проверка последовательности на случайность и равномерность
def test3(x, m, K, r, alpha):
    n = len(x) 
    passed = True
    # Результат прохождения тестов на каждой подпоследовательности (итериции)
    iters_info = []
    i = 0
    t = len(x) // r
    while i < r and passed == True:
        # Результаты тестов на текущей подпоследовательности
        test1_pass = test1(x[i * t:(i+1) * t], m, alpha)
        test2_pass = test2(x[i * t:(i+1) * t], m, K, alpha)
        if not (test1_pass and test2_pass):
            passed = False
        iters_info.append([i, test1_pass[-1], test2_pass[-1]])
        i += 1
    return n, m, K, r, iters_info, passed


# Метод Стёрджесса для определения длины интервалов для хи-квадрата
def sturgess_method(n):
    return floor(1 + log2(n))


# Тест критерия типа хи-квадрат
def chi2_test(x, m, alpha):
    n = len(x)
    # Получения количества интервалов разбиения
    K = sturgess_method(n)
     # Торетическая вероятность попадания в интервал
    E = 1 / K
    # Относительные частоты попадания в интервал
    v = calc_frequencies(x, m, K)
    # Расчёт значения статистики критерия хи-квадрат
    S = n * sum([(O - E)**2 / E for O in v])
    r = K - 1
    integral_res = quad(lambda S: S**(r / 2 - 1) * exp(-S / 2), S, inf)[0]
    S_alpha = integral_res / (2**(r / 2) * gamma(r / 2))
    passed = alpha < S_alpha
    return n, m, K, E, v, S, S_alpha, passed


# Разность между накопленными частотами
def calc_D(x, m):
    n = len(x)
    D_plus = max([(i+1) / n - x[i] / m for i in range(n)])
    D_minus = max([x[i] / m - i / n for i in range(n)])
    return max(D_plus, D_minus)


# Тест критерия Колмогорова
def kolmogorov_test(x, m, alpha):
    n = len(x)
    sort_x = sorted(x)
    # Масимальнуая разность между накопленными частотами
    D = calc_D(sort_x, m)
    n = len(sort_x)
    # Расчёт значения статистики критерия хи-квадрат
    S = (n * D + 1) / sqrt(n)
    S_alpha = 1 - nsum(lambda k: (-1)**k * exp(-2 * k**2 * S**2), [-inf,  inf])
    passed = alpha < S_alpha
    return n, m, D, S, S_alpha, passed