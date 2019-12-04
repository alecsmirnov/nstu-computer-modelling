import matplotlib.pyplot as plt
from numpy import arange
from sys import exit


def str_to_bool(str):
    return True if str == "True" else False
    

def get_filename(distr_filename, filename, n=0):
    result = distr_filename
    if n != 0:
        result += "_" + str(n)
    result += "_" + filename
    return result


def draw_chart(picturename, title, x_label, y_label, func, *args):
    X_MAX = 10
    X_STEP = 0.05
    x = arange(0, X_MAX + X_STEP, X_STEP) 
    plt.xticks(range(0, X_MAX + 1))
    plt.title(title)
    plt.xlabel(x_label) 
    plt.ylabel(y_label)
    y = [func(x, *args) for x in x]
    plt.plot(x, y)
    plt.grid(True)
    plt.savefig(picturename)
    plt.clf()
    plt.close()


def draw_histogram(picturename, title, intervals, v, theor_intervals, theor_v, bar_width):
    plt.title(title)
    plt.xlabel("Интервалы")
    plt.ylabel("Частоты")
    plt.xticks(intervals, rotation=90)
    plt.plot(theor_intervals[:len(theor_intervals) - 1], theor_v, marker="o", label="Теоритическая")
    plt.bar(intervals[:len(intervals) - 1], v, width=bar_width, alpha=0.5, 
            align="edge", edgecolor="grey", color="lightgrey", label="Эмпирическая")
    plt.legend(loc="best", frameon=True)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(picturename)
    plt.clf()
    plt.close()


# Запись результатов выполнения тестов (Хи-квадрат и Крамера-Мизеса-Смирнов)
def write_tests_results(filename, precision, arg_list, arg_labels, alpha, sequence, intervals, hits, modeling_time,
                        chi2_r, chi2_S, chi2_PSS, chi2_passed, cms_S, cms_PSS, cms_passed):
    n = len(sequence)
    f = open(filename, "w")
    f.write("Квантиль распределения (alpha): {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    for i in range(len(arg_list)):
        f.write("Параметры распределения ({0}): {1}\n".format(arg_labels[i], arg_list[i]))
    f.write("\nПоследовательность: {0}\n".format([round(i, precision) for i in sequence]))
    f.write("Интервалы: {0}\n".format([round(i, precision) for i in intervals]))
    f.write("Попадания в интервалы: {0}\n".format([round(i, precision) for i in hits]))
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
    f.write("\nПроверка гипотезы по критерию Крамера-Мизеса-Смирнова\n")
    f.write("Значение S: {0}\n".format(round(cms_S, precision)))
    f.write("Значение P{{S > S*}}: {0}\n".format(round(cms_PSS, precision)))
    if cms_passed == True:
        f.write("Гипотеза не отвергается: P{{S > S*}} > alpha = {0} > {1}\n".format(round(cms_PSS, precision), alpha))
    else:
        f.write("Гипотеза отвергается: P{{S > S*}} < alpha = {0} < {1}\n".format(round(cms_PSS, precision), alpha))
    f.write("Результат прохождения теста: {0}".format(cms_passed))
    f.close()