import matplotlib.pyplot as plt
from numpy import arange
from sys import exit


# Перевод стокового логического значения в булевое
def str_to_bool(str):
    return True if str == "True" else False


# Отрисовка гистограммы по заданным относительным частотам попадания в интервал
def draw_histogram(picturename, data, n=0, m=0):
    x = arange(len(data))
    data_min = min([x for x in data if x != 0])
    plt.bar(x, height=data, width=1, align="edge") 
    plt.xticks(x)
    plt.yticks(arange(0, max(data) + data_min, step=data_min/2))
    title = "Частотная гистограмма"
    if n != 0 and m != 0:
        title += " (n = {0}, m = {1})".format(n, m)
    plt.title(title)
    plt.xlabel("Количество интервалов (K)")
    plt.ylabel("Относительные частоты (v)")
    plt.grid(True)
    plt.savefig(picturename)
    plt.clf()


# Записать последовательность в файл
def write_sequence(filename, seq):
    with open(filename, "w") as f:
        for value in seq:
            f.write("%s " % value)


# Записать в файл результаты тестирования последовательности
def write_analysis_result(filename, x0, a, b, c, n, m, T_len, T_len_min, tests_result):
    with open(filename, "w") as f:
        f.write("Последовательность с параметрами:\n")
        f.write("x0: {0}\n".format(x0))
        f.write("a: {0}\n".format(a))
        f.write("b: {0}\n".format(b))
        f.write("c: {0}\n".format(c))
        f.write("n (Длина): {0}\n".format(n))
        f.write("m (Основание): {0}\n".format(n))
        f.write("T (Длина периода): {0}\n".format(T_len))
        f.write("\nКоличество испытаний: {0}\n".format(T_len_min))
        if tests_result != []:
            f.write("\nРезультаты тестов:\n")
            f.write("1) Тест 1: {0}\n".format(tests_result[0]))
            f.write("2) Тест 2: {0}\n".format(tests_result[1]))
            f.write("3) Тест 3: {0}\n".format(tests_result[2]))
            f.write("4) Хи-квадрат тест: {0}\n".format(tests_result[3]))
            f.write("5) Тест Колмогорова: {0}\n".format(tests_result[4]))
        else:
            f.write("\nПериод сгенерированной последовательности меньше чем {0}!\n".format(T_len))


# Записать в файл результаты теста 1
def write_test1_results(filename, precision, alpha, n, Q, a, b, passed):
    f = open(filename, "w")
    f.write("Квантиль уровня (1 - alpha / 2) нормального распределения: {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    f.write("Количество перестановок (Q): {0}\n".format(Q))
    f.write("Доверительный интервал: [{0}; {1}]\n".format(round(a, precision), round(b, precision)))
    f.write("Значение (n / 2): {0}\n".format(round(n / 2, precision)))
    if passed == True:
        hit_text = "Значение попадает в доверительный интервал: {0} <= {1} <= {2}\n"
        f.write(hit_text.format(round(a, precision), round(n / 2, precision), round(b, precision)))
    else:
        miss_text = "Значение не попадает в доверительный интервал: {0} < {1} < {2}\n"
        if n / 2 < a:
            f.write(miss_text.format(round(n / 2, precision), round(a, precision), round(b, precision)))
        else:
            f.write(miss_text.format(round(a, precision), round(b, precision), round(n / 2, precision)))
    f.write("\nРезультат прохождения теста: {0}".format(passed))
    f.close()


# Записать в файл результаты теста 2
def write_test2_results(filename, precision, alpha, n, m, K, 
                        v, freq_table, freq_pass, 
                        MX, MX_a, MX_b, MX_val, MX_pass, 
                        DX, DX_a, DX_b, DX_val, DX_pass, passed):
    f = open(filename, "w")
    f.write("Квантиль уровня (1 - alpha / 2) нормального распределения: {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    f.write("Основание последовательности (m): {0}\n".format(m))
    f.write("Количество интервалов (K): {0}\n".format(K))
    f.write("Относительные частоты попадания в интервал (v): {0}\n".format(str(v).strip('[]')))
    f.write("Таблица попадания частот:\n")
    for item in freq_table:
        f.write("{0}:\t[{1}; {2}], vi = {3}:\t{4}\n".format(item[0], round(item[1], precision), round(item[2], precision), round(item[3], precision), item[4]))
    f.write("Результат прохождения частотного теста: {0}\n".format(freq_pass))
    f.write("\nМатематическое ожидание (MX): {0}\n".format(round(MX, precision)))
    f.write("Доверительный интервал: [{0}; {1}]\n".format(round(MX_a, precision), round(MX_b, precision)))
    f.write("Значение (m / 2): {0}\n".format(round(MX_val, precision)))
    if MX_pass == True:
        hit_text = "Значение попадает в доверительный интервал: {0} <= {1} <= {2}\n"
        f.write(hit_text.format(round(MX_a, precision), round(MX_val, precision), round(MX_b, precision)))
    else:
        miss_text = "Значение не попадает в доверительный интервал: {0} < {1} < {2}\n"
        if MX_val < MX_a:
            f.write(miss_text.format(round(MX_val, precision), round(MX_a, precision), round(MX_b, precision)))
        else:
            f.write(miss_text.format(round(MX_a, precision), round(MX_b, precision), round(MX_val, precision)))
    f.write("Результат оценки сходимости мат ожидания: {0}\n".format(MX_pass))
    f.write("\nДисперсия (DX): {0}\n".format(round(DX, precision)))
    f.write("Доверительный интервал: [{0}; {1}]\n".format(round(DX_a, precision), round(DX_b, precision)))
    f.write("Значение (m^2 / 12): {0}\n".format(round(DX_val, precision)))
    if DX_pass == True:
        hit_text = "Значение попадает в доверительный интервал: {0} <= {1} <= {2}\n"
        f.write(hit_text.format(round(DX_a, precision), round(DX_val, precision), round(DX_b, precision)))
    else:
        miss_text = "Значение не попадает в доверительный интервал: {0} < {1} < {2}\n"
        if DX_val < DX_a:
            f.write(miss_text.format(round(DX_val, precision), round(DX_a, precision), round(DX_b, precision)))
        else:
            f.write(miss_text.format(round(DX_a, precision), round(DX_b, precision), round(DX_val, precision)))
    f.write("Результат оценки сходимости дисперсии: {0}\n".format(DX_pass))
    f.write("\nРезультат прохождения теста: {0}".format(passed))
    f.close()


# Записать в файл результаты теста 3
def write_test3_results(filename, _, alpha, n, m, K, r, iters_info, passed):
    f = open(filename, "w")
    f.write("Квантиль уровня (1 - alpha / 2) нормального распределения: {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    f.write("Основание последовательности (m): {0}\n".format(m))
    f.write("Количество интервалов (K): {0}\n".format(K))
    f.write("Количество подпоследовательностей (r): {0}\n".format(r))
    f.write("Результат прохождения тестов для каждой подпоследовательности:\n")
    f.write("i\tTecт 1\tТест 2\n")
    for iter in iters_info:
        f.write("{0}\t{1}\t{2}\n".format(iter[0], iter[1], iter[2]))
    f.write("\nРезультат прохождения теста: {0}".format(passed))
    f.close()


# Записать в файл результаты хи-квадрат теста
def write_chi2_results(filename, precision, alpha, n, m, K, E, v, S, S_alpha, passed):
    f = open(filename, "w")
    f.write("Квантиль хи-квадрат распределения (alpha): {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    f.write("Основание последовательности (m): {0}\n".format(m))
    f.write("Количество интервалов (K): {0}\n".format(K))
    f.write("Степени свободы (r): {0}\n".format(K - 1))
    f.write("\nТеоретическая вероятность попадания в интервал (E): {0}\n".format(round(E, precision)))
    f.write("Относительные частоты попадания в интервал (v): {0}\n".format(str(v).strip('[]')))
    f.write("\nЗначение P{{S > S*}}: {0}\n".format(round(S_alpha, precision)))
    if passed == True:
        f.write("Гипотеза не отвергается: P{{S > S*}} > alpha = {0} > {1}\n".format(round(S_alpha, precision), alpha))
    else:
        f.write("Гипотеза отвергается: P{{S > S*}} < alpha = {0} < {1}\n".format(round(S_alpha, precision), alpha))
    f.write("\nРезультат прохождения теста: {0}".format(passed))
    f.close()


# Записать в файл результаты теста Колмогорова
def write_kolmogorov_results(filename, precision, alpha, n, m, D, S, S_alpha, passed):
    f = open(filename, "w")
    f.write("Верхние процентные точки (alpha): {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    f.write("Основание последовательности (m): {0}\n".format(m))
    f.write("Разность между накопленными частотами (D): {0}\n".format(round(D, precision)))
    f.write("\nЗначение P{{S > S*}}: {0}\n".format(round(S_alpha, precision)))
    if passed == True:
        f.write("Гипотеза не отвергается: P{{S > S*}} > alpha = {0} > {1}\n".format(round(S_alpha, precision), alpha))
    else:
        f.write("Гипотеза отвергается: P{{S > S*}} < alpha = {0} < {1}\n".format(round(S_alpha, precision), alpha))
    f.write("\nРезультат прохождения теста: {0}".format(passed))
    f.close()