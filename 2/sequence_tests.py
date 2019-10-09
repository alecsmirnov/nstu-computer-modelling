import math
import scipy.stats as st
import numpy as np
import matplotlib.pyplot as plt
import file_functions as ff


# Директории для входных и выходных данных
INPUT_PATH  = "input/"
OUTPUT_PATH = "output/"

# Названия файлов для результатов тестов
TEST1_RESULT_FILE           = OUTPUT_PATH + "test1_result.txt"
TEST2_RESULT_FILE           = OUTPUT_PATH + "test2_result.txt"
TEST3_RESULT_FILE           = OUTPUT_PATH + "test3_result.txt"
CHI2_TEST_RESULT_FILE       = OUTPUT_PATH + "chi2_test_result.txt"
KOLMOGOROV_TEST_RESULT_FILE = OUTPUT_PATH + "kolmogorov_test_result.txt"

# Названия файлов с изображением гистограм
TEST2_HISTOGRAM     = OUTPUT_PATH + "test2_histogram.png"
CHI2_TEST_HISTOGRAM = OUTPUT_PATH + "chi2_test_histogram.png"

# Точность отображаемых результатов выходных данных
PRECISION = 3


# Отрисовка гистограммы по заданным относительным частотам попадания в интервал
def draw_histogram(picturename, data, n=0, m=0):
    x = np.arange(len(data))
    data_min = min([x for x in data if x != 0])
    plt.bar(x, height=data, width=1, align="edge") 
    plt.xticks(x)
    plt.yticks(np.arange(0, max(data) + data_min, step=data_min/2))
    title = "Frequency histogram"
    if n != 0 and m != 0:
        title += " (n = {0}, m = {1})".format(n, m)
    plt.title(title)
    plt.xlabel("Intervals (K)")
    plt.ylabel("Hit frequency (v)")
    plt.grid(True)
    plt.savefig(picturename)
    plt.clf()


# Тест проверки перестановок
def test1(x, alpha, output=True):
    n = len(x)
    # Квантиль нормального распределения уровня 1 - alpha / 2
    U = st.norm.ppf(1 - alpha / 2)
    # Количество перестановок
    Q = 0
    for i in range(n - 1): 
        if x[i] > x[i+1]:
            Q += 1
    # Доверительный интервал по смоделированной выборке оценке числа перестановок Q
    a = Q - U * math.sqrt(n) / 2
    b = Q + U * math.sqrt(n) / 2
    # Проверка попадания оценки в доверительный интервал
    passed = a <= n / 2 <= b
    if output == True:
        ff.write_test1_results(TEST1_RESULT_FILE, PRECISION, alpha, n, Q, a, b, n / 2, passed)
    return passed


# Поиск математического ожидания последовательности
def calc_MX(x):
    return sum(x) / len(x)


# Поиск дисперсии последовательности
def calc_DX(x):
    MX = calc_MX(x)
    return sum([(x - MX)**2 for x in x]) / (len(x) - 1)


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
    errors = []
    # Квантиль нормального распределения уровня 1 - alpha / 2
    U = st.norm.ppf(1 - alpha / 2)
    for i in range(K):
        # Построение доверительного интервала
        a = v[i] - U / K * math.sqrt(K - 1 / n) 
        b = v[i] + U / K * math.sqrt(K - 1 / n)
        # Проверка попадания частоты в доверительный интервал
        if not (a <= 1 / K <= b): 
            errors.append(v[i])
    return errors == [], errors


# Тест оценки сходимости математического ожидания
def MX_estimate_test(MX, DX, n, m, alpha):
    # Квантиль нормального распределения уровня 1 - alpha / 2
    U = st.norm.ppf(1 - alpha / 2)
    # Построение доверительного интервала
    a = MX - U * math.sqrt(DX) / math.sqrt(n)
    b = MX + U * math.sqrt(DX) / math.sqrt(n) 
    return a <= m / 2 <= b, a, b, m / 2


# Тест оценки сходимости дисперсии
def DX_estimate_test(DX, n, m, alpha):
    # Построение доверительного интервала
    a = (n - 1) * DX / st.chi2.isf(alpha / 2, n - 1)
    b = (n - 1) * DX / st.chi2.isf(1 - alpha / 2, n - 1)
    return a <= m**2 / 12 <= b, a, b, m**2 / 12


# Тест на равномерность 
def test2(x, m, K, alpha, plot=False, output=True):
    # Расчёт мат ожидания
    MX = calc_MX(x)
    # Расчёт дисперсии
    DX = calc_DX(x)
    # Получение относительных частот попадания в интервал
    v = calc_frequencies(x, m, K)
    n = len(x) 
    # Результаты частотного теста
    freq_pass, freq_errs = frequencies_test(v, n, m, K, alpha)
    # Результаты теста оценки сходимости математического ожидания
    MX_pass, MX_a, MX_b, MX_val = MX_estimate_test(MX, DX, n, m, alpha)
    # Результаты теста оценки сходимости дисперсии
    DX_pass, DX_a, DX_b, DX_val = DX_estimate_test(DX, n, m, alpha)
    passed = freq_pass and MX_pass and DX_pass
    if plot == True:
        draw_histogram(TEST2_HISTOGRAM, v, n, m) 
    if output == True:
        ff.write_test2_results(TEST2_RESULT_FILE, PRECISION, alpha, n, m, K, 
                           v, freq_pass, freq_errs,
                           MX, MX_pass, MX_a, MX_b, MX_val, 
                           DX, DX_pass, DX_a, DX_b, DX_val, passed)
    return passed


# Проверка последовательности на случайность и равномерность
def test3(x, m, K, r, alpha, output=True):
    passed = True
    # Результат прохождения тестов на каждой подпоследовательности (итериции)
    iters_info = []
    i = 0
    t = len(x) // r
    while i < r and passed == True:
        # Результаты тестов на текущей подпоследовательности
        test1_pass = test1(x[i * t:(i+1) * t], alpha, output=False)
        test2_pass = test2(x[i * t:(i+1) * t], m, K, alpha, output=False)
        if not (test1_pass and test2_pass):
            passed = False
        if output == True:
            iters_info.append([i, test1_pass, test2_pass])
        i += 1
    if output == True:
        ff.write_test3_results(TEST3_RESULT_FILE, alpha, len(x), m, K, r, iters_info, passed)
    return passed


# Метод Стёрджесса для определения длины интервалов для хи-квадрата
def sturgess_method(n):
    return math.floor(1 + math.log2(n))


# Тест критерия типа хи-квадрат
def chi2_test(x, m, alpha, plot=False, output=False):
    n = len(x)
    # Получения количества интервалов разбиения
    K = sturgess_method(n)
     # Торетическая вероятность попадания в интервал
    E = 1 / K
    # Относительные частоты попадания в интервал
    v = calc_frequencies(x, m, K)
    # Расчёт значения статистики критерия хи-квадрат
    S = n * sum([(O - E)**2 / E for O in v])
    # Критическое значение 
    S_alpha = st.chi2.isf(alpha, K - 1)
    passed = S < S_alpha
    if plot == True:
        draw_histogram(CHI2_TEST_HISTOGRAM, v, n, m) 
    if output == True:
        ff.write_chi2_results(CHI2_TEST_RESULT_FILE, PRECISION, alpha, n, m, K, E, v, S, S_alpha, passed)
    return passed


# Разность между накопленными частотами
def calc_D(x, m):
    n = len(x)
    D_plus = max([(i+1) / n - x[i] / m for i in range(n)])
    D_minus = max([x[i] / m - i / n for i in range(n)])
    return max(D_plus, D_minus)


# Тест критерия Колмогорова
def kolmogorov_test(x, m, alpha, output=True):
    # Критические значения при заданных уровнях значимости
    S_alpha = {0.15: 1.1379, 0.1: 1.2238, 0.05: 1.3581, 0.025: 1.4802, 0.01: 1.6276}
    # Расположение наблюдений в порядке возрастания
    sort_x = sorted(x)
    # Масимальнуая разность между накопленными частотами
    D = calc_D(sort_x, m)
    n = len(sort_x)
    # Расчёт значения статистики критерия хи-квадрат
    S = (n * D + 1) / math.sqrt(n)
    passed = S < S_alpha[alpha]
    if output == True:
        ff.write_kolmogorov_results(KOLMOGOROV_TEST_RESULT_FILE, PRECISION, alpha, n, m, D, S, S_alpha[alpha], passed)
    return passed