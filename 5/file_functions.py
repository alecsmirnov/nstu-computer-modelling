import matplotlib.pyplot as plt
from numpy import arange
from sys import exit


def str_to_bool(str):
    return True if str == "True" else False


def draw_histogram(picturename, intervals, v, theor_intervals, theor_v, bar_width):
    plt.xlabel("Интервалы")
    plt.ylabel("Частоты")
    plt.xticks(intervals, rotation=90)
    plt.plot(theor_intervals, theor_v, marker="o", label="Теоритическая")
    plt.bar(intervals[:len(intervals) - 1], v, width=bar_width, alpha=0.5, 
            align="edge", edgecolor="grey", color="lightgrey", label="Эмпирическая")
    plt.legend(loc="best", frameon=True)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(picturename)
    plt.clf()
    plt.close()
    

def draw_chart(picturename, title, x_label, y_label, a, b, func, mu, sigm):
    x = arange(a, b, 0.01) 
    y = [func(x, mu, sigm) for x in x]
    plt.title(title + " (μ = {0}; σ = {1})".format(mu, sigm))
    plt.xlabel(x_label) 
    plt.ylabel(y_label)
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
        exit()
    # Длина поселдовательности
    n = int(f.readline())
    # Параметры распределения
    mu = float(f.readline())
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
    return n, mu, sigm, alpha, precision, histogram_run, charts_run


# Запись результатов выполнения тестов (Хи-квадрат и Смирнова)
def write_tests_results(filename, precision, mu, sigm, alpha, a, b, sequence, density, count, intervals, hits, modeling_time,
                        chi2_r, chi2_S, chi2_PSS, chi2_passed, sm_S, sm_PSS, sm_passed):
    n = len(sequence)
    f = open(filename, "w")
    f.write("Квантиль распределения (alpha): {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    f.write("Параметры распределения (mu): {0}\n".format(mu))
    f.write("Параметры распределения (sigma): {0}\n".format(sigm))
    f.write("\nПоследовательность: {0}\n".format([round(i, precision) for i in sequence]))
    f.write("Интервалы: {0}\n".format([round(i, precision) for i in intervals]))
    f.write("Попадания в интервалы: {0}\n".format([round(i, precision) for i in hits]))

    f.write("Границы отрезков моделирования: [{0}, {1}]\n".format(round(a, precision), round(b, precision)))
    f.write("G_={{(x, y): 0 <= y <= {0}}}\n".format(round(density, precision)))
    f.write("Количество сгенерированных величин: {0}\n".format(count))

    f.write("\nВремя моделирования последовательности (sec): {0}\n".format(round(modeling_time, precision)))
    f.write("\nПроверка гипотезы по критерию Хи-квадрат\n")
    f.write("Значение r: {0}\n".format(round(chi2_r, precision)))
    f.write("Значение S: {0}\n".format(round(chi2_S, precision)))
    f.write("Значение P{{S > S*}}: {0}\n".format(round(chi2_PSS, precision)))
    if chi2_passed == True:
        f.write("Гипотеза не отвергается: P{{S > S*}} > alpha = {0} > {1}\n".format(round(chi2_PSS, precision), alpha))
    else:
        f.write("Гипотеза отвергается: P{{S > S*}} < alpha = {0} < {1}\n".format(round(chi2_PSS, precision), alpha))
    f.write("Результат прохождения теста: {0}\n".format(chi2_passed))
    f.write("\nПроверка гипотезы по критерию Смирнова\n")
    f.write("Значение S: {0}\n".format(round(sm_S, precision)))
    f.write("Значение P{{S > S*}}: {0}\n".format(round(sm_PSS, precision)))
    if sm_passed == True:
        f.write("Гипотеза не отвергается: P{{S > S*}} > alpha = {0} > {1}\n".format(round(sm_PSS, precision), alpha))
    else:
        f.write("Гипотеза отвергается: P{{S > S*}} < alpha = {0} < {1}\n".format(round(sm_PSS, precision), alpha))
    f.write("Результат прохождения теста: {0}".format(sm_passed))
    f.close()