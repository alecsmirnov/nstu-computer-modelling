import sys
import numpy as np
import matplotlib.pyplot as plt


def str_to_bool(str):
    return True if str == "True" else False


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


def draw_chart(picturename, title, x_label, y_label, func, *arg):
    X_MAX = 10
    X_STEP = 0.01
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


# Чтение данных для выполняемых тестов
def read_tests_settings(filename):
    try:
        f = open(filename, "r")
    except IOError:
        print("Невозможно открыть файл: {0}".format(filename))
        sys.exit()
    # Длина поселдовательности
    n = int(f.readline())
    # Параметр распределения
    sigm = float(f.readline())
    # Уровень значимости
    alpha = float(f.readline())
    # Точность вычислений
    precision = int(f.readline())
    # Отрисовка гистограммы
    histogram_run = str_to_bool(f.readline().rstrip('\n'))
    # Отрисовка графиков функции
    charts_run = str_to_bool(f.readline().rstrip('\n'))
    f.close()
    return n, sigm, alpha, precision, histogram_run, charts_run


# Запись результатов выполнения тестов (Хи-квадрат и Андерса-Дарлинга)
def write_tests_results(filename, precision, sigm, alpha, sequence, intervals, hits, modeling_time,
                        chi2_S, chi2_PSS, chi2_passed, ad_S, ad_PSS, ad_passed):
    n = len(sequence)
    f = open(filename, "w")
    f.write("Квантиль распределения (alpha): {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    f.write("Параметры распределения (sigma): {0}\n".format(sigm))
    f.write("\nПоследовательность: {0}\n".format([round(i, precision) for i in sequence]))
    f.write("Интервалы: {0}\n".format([round(i, precision) for i in intervals]))
    f.write("Попадания в интервалы: {0}\n".format([round(i, precision) for i in hits]))
    f.write("\nВремя моделирования последовательности (sec): {0}\n".format(round(modeling_time, precision)))
    f.write("\nПроверка гипотезы по критерию Хи-квадрат\n")
    f.write("Значение S: {0}\n".format(round(chi2_S, precision)))
    f.write("Значение P{{S > S*}}: {0}\n".format(round(chi2_PSS, precision)))
    if chi2_passed == True:
        f.write("Гипотеза не отвергается: P{{S > S*}} > alpha = {0} > {1}\n".format(round(chi2_PSS, precision), alpha))
    else:
        f.write("Гипотеза отвергается: P{{S > S*}} < alpha = {0} < {1}\n".format(round(chi2_PSS, precision), alpha))
    f.write("Результат прохождения теста: {0}\n".format(chi2_passed))
    f.write("\nПроверка гипотезы по критерию Омера-квадрат Андерсона-Дарлинга\n")
    f.write("Значение S: {0}\n".format(round(ad_S, precision)))
    f.write("Значение P{{S > S*}}: {0}\n".format(round(ad_PSS, precision)))
    if ad_passed == True:
        f.write("Гипотеза не отвергается: P{{S > S*}} > alpha = {0} > {1}\n".format(round(ad_PSS, precision), alpha))
    else:
        f.write("Гипотеза отвергается: P{{S > S*}} < alpha = {0} < {1}\n".format(round(ad_PSS, precision), alpha))
    f.write("Результат прохождения теста: {0}".format(ad_passed))
    f.close()