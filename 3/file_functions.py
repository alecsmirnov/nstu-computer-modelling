import sys
import numpy as np
import matplotlib.pyplot as plt

# Отсутствие параметра для вывода результата
NONE = 0


def draw_histogram(picturename, intervals, v, theor_intervals, theor_v):
    plt.xlabel("Количество интервалов")
    plt.ylabel("Частоты")
    plt.xticks(np.arange(max(intervals) + 2))
    plt.plot(theor_intervals, theor_v, marker="o")
    plt.bar(intervals, v, width=1, align="center", edgecolor="grey", color="lightgrey")
    plt.grid(True)
    plt.savefig(picturename)
    plt.clf()


# Чтение данных для выполняемых тестов
def read_tests_settings(filename):
    try:
        f = open(filename, "r")
    except IOError:
        print("Невозможно открыть файл: {0}".format(filename))
        sys.exit()
    # Длина поселдовательности
    n = int(f.readline())
    # Параметры Биномиального распределения
    m = int(f.readline())
    p = float(f.readline())
    # Параметр распределения Пуассона
    lambd = int(f.readline())
    # Уровень значимости
    alpha = float(f.readline())
    # Точность вычислений
    precision = int(f.readline())
    f.close()
    return n, m, p, lambd, alpha, precision


# Запись результатов выполнения теста хи-квадрат
def write_chi2_results(filename, precision, sequence, P, alpha, n, m, p, lambd, 
                       S, S_alpha, implement_count, v, interval_hits, operations_count, passed):
    f = open(filename, "w")
    f.write("Квантиль хи-квадрат распределения (alpha): {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    if m != 0 and p != 0:     
        f.write("Параметры распределения: m = {0}, p = {1}\n".format(m, p))
    if lambd != 0:
        f.write("Параметры распределения Пуассона (lambda): {0}\n".format(lambd))
    f.write("\nПоследовательность: {0}\n".format(sequence))
    f.write("Вероятности: {0}\n".format([round(i, precision) for i in P]))
    f.write("Сумма вероятностей: {0}\n".format(round(sum(P), precision)))
    f.write("Количество попаданий в интервал: {0}\n".format(dict(interval_hits)))
    f.write("Относительные частоты попадания в интервал (v): {0}\n".format(str(v).strip('[]')))
    f.write("\nКоличество операций: {0}\n".format(operations_count))
    f.write("\nСтепени свободы (r): {0}\n".format(implement_count - 1))
    f.write("Значение S: {0}\n".format(round(S, precision)))
    f.write("Значение P{{S > S*}}: {0}\n".format(round(S_alpha, precision)))
    if passed == True:
        f.write("Гипотеза не отвергается: P{{S > S*}} > alpha = {0} > {1}\n".format(round(S_alpha, precision), alpha))
    else:
        f.write("Гипотеза отвергается: P{{S > S*}} < alpha = {0} < {1}\n".format(round(S_alpha, precision), alpha))
    f.write("\nРезультат прохождения теста: {0}".format(passed))
    f.close()