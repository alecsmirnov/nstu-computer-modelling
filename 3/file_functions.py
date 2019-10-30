import sys


def write_chi2_results(filename, precision, sequence, P, alpha, n, m, p, lambd, v, S_alpha, 
                       implement_count, interval_hits, passed):
    f = open(filename, "w")
    f.write("Квантиль хи-квадрат распределения (alpha): {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    if m != 0 and p != 0:     
        f.write("Параметры распределения: m = {0}, p = {1}\n".format(m, p))
    if lambd != 0:
        f.write("Параметры распределения Пуассона (λ): {0}\n".format(lambd))
    f.write("Последовательность: {0}\n".format(sequence))
    f.write("Вероятности: {0}\n".format([round(i, precision) for i in P]))
    f.write("Количество попаданий в интервал: {0}\n".format(dict(interval_hits)))
    f.write("Относительные частоты попадания в интервал (v): {0}\n".format(str(v).strip('[]')))
    f.write("Степени свободы (r): {0}\n".format(implement_count - 1))

    f.write("\nЗначение P{{S > S*}}: {0}\n".format(round(S_alpha, precision)))
    if passed == True:
        f.write("Гипотеза не отвергается: P{{S > S*}} > alpha = {0} > {1}\n".format(round(S_alpha, precision), alpha))
    else:
        f.write("Гипотеза отвергается: P{{S > S*}} < alpha = {0} < {1}\n".format(round(S_alpha, precision), alpha))
    f.write("\nРезультат прохождения теста: {0}".format(passed))
    f.close()