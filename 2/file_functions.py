import sys


# Перевод стокового логического значения в булевое
def str_to_bool(str):
    return True if str == "True" else False


# Чтение данных для генератора псевдослучайных чисел
def read_generator_settings(filename):
    try:
        f = open(filename, "r")
    except IOError:
        print("Невозможно открыть файл: ", filename)
        sys.exit()
    # Начальный элемент последовательности
    x0 = int(f.readline())
    # Коэффициенты генератора
    a, b, c = [int(x) for x in f.readline().split()]
    # Длина и Основание последователности
    n, m = [int(x) for x in f.readline().split()]
    f.close()
    return  x0, a, b, c, n, m


# Чтение данных для выполняемых тестов
def read_tests_settings(filename):
    try:
        f = open(filename, "r")
    except IOError:
        print("Невозможно открыть файл: ", filename)
        sys.exit()
    # Количество тестов
    TESTS_COUNT = 5
    tests_data = [[] for i in range(TESTS_COUNT)]
    # Получаем длину допустимого периода последовательности
    T_len = int(f.readline())
    # Данные для теста 1: alpha
    tests_data[0].append(float(f.readline()))
    data_temp = f.readline().split()
    # Данные для теста 2: K, alpha, логическое условие рисования графика
    tests_data[1].append(int(data_temp[0]))
    tests_data[1].append(float(data_temp[1]))
    tests_data[1].append(str_to_bool(data_temp[2]))
    # Данные для теста 3: К, r, alpha
    data_temp = f.readline().split()
    tests_data[2].append(int(data_temp[0]))
    tests_data[2].append(int(data_temp[1]))
    tests_data[2].append(float(data_temp[2]))
    # Данные для хи^2-теста: alpha, логическое условие рисования графика
    data_temp = f.readline().split()
    tests_data[3].append(float(data_temp[0]))
    tests_data[3].append(str_to_bool(data_temp[1]))
    # Данные для теста Колмогорова: alpha
    tests_data[4].append(float(f.readline()))
    f.close()
    return  T_len, tests_data


# Записать последовательность в файл
def write_sequence(filename, seq):
    with open(filename, "w") as f:
        for value in seq:
            f.write("%s " % value)


# Записать в файл результаты тестирования последовательности
def write_analysis_result(filename, x0, a, b, c, n, m, T_len, tests_result):
    with open(filename, "w") as f:
        f.write("Последовательность с параметрами:\n")
        f.write("x0: {0}\n".format(x0))
        f.write("a: {0}\n".format(a))
        f.write("b: {0}\n".format(b))
        f.write("c: {0}\n".format(c))
        f.write("n (Длина): {0}\n".format(n))
        f.write("m (Основание): {0}\n".format(n))
        f.write("len(T) (Длина периода): {0}\n".format(T_len))
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
def write_test1_results(filename, precision, alpha, n, Q, a, b, val, passed):
    f = open(filename, "w")
    f.write("Квантиль уровня (1 - alpha / 2) нормального распределения: {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    f.write("Количество перестановок (Q): {0}\n".format(Q))
    f.write("Доверительный интервал: [{0}; {1}]\n".format(round(a, precision), round(b, precision)))
    f.write("Значение (n / 2): {0}\n".format(round(val, precision)))
    if passed == True:
        hit_text = "Значение попадает в доверительный интервал: {0} <= {1} <= {2}\n"
        f.write(hit_text.format(round(a, precision), round(val, precision), round(b, precision)))
    else:
        miss_text = "Значение не попадает в доверительный интервал: {0} < {1} < {2}\n"
        if val < a:
            f.write(miss_text.format(round(val, precision), round(a, precision), round(b, precision)))
        else:
            f.write(miss_text.format(round(a, precision), round(b, precision), round(val, precision)))
    f.write("\nРезульт прохождения теста: {0}".format(passed))
    f.close()


# Записать в файл результаты теста 2
def write_test2_results(filename, precision, alpha, n, m, K,
                       v, freq_pass, freq_table, 
                       MX, MX_pass, MX_a, MX_b, MX_val, 
                       DX, DX_pass, DX_a, DX_b, DX_val, passed):
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
    f.write("\nРезульт прохождения теста: {0}".format(passed))
    f.close()


# Записать в файл результаты теста 3
def write_test3_results(filename, alpha, n, m, K, r, iters_info, passed):
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
    f.write("\nРезульт прохождения теста: {0}".format(passed))
    f.close()


# Записать в файл результаты хи-квадрат теста
def write_chi2_results(filename, precision, alpha, n, m, K, E, v, S, S_alpha, passed):
    f = open(filename, "w")
    f.write("Квантель хи-квадрат распределения (alpha): {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    f.write("Основание последовательности (m): {0}\n".format(m))
    f.write("Количество интервалов (K): {0}\n".format(K))
    f.write("Степени свободы (r): {0}\n".format(K - 1))
    f.write("\nТеоретическая вероятность попадания в интервал (E): {0}\n".format(round(E, precision)))
    f.write("Относительные частоты попадания в интервал (v): {0}\n".format(str(v).strip('[]')))
    f.write("\nЗначение статистики критерия (S): {0}\n".format(round(S, precision)))
    f.write("Критическое значение (S_alpha): {0}\n".format(round(S_alpha, precision)))
    if passed == True:
        f.write("Гипотеза не отвергается: S < S_alpha = {0} < {1}\n".format(round(S, precision), round(S_alpha, precision)))
    else:
        f.write("Гипотеза отвергается: S > S_alpha = {0} > {1}\n".format(round(S, precision), round(S_alpha, precision)))
    f.write("\nРезульт прохождения теста: {0}".format(passed))
    f.close()


# Записать в файл результаты теста Колмогорова
def write_kolmogorov_results(filename, precision, alpha, n, m, D, S, S_alpha, passed):
    f = open(filename, "w")
    f.write("Верхние процентные точки (alpha): {0}\n".format(alpha))
    f.write("Количество элементов (n): {0}\n".format(n))
    f.write("Основание последовательности (m): {0}\n".format(m))
    f.write("Разность между накопленными частотами (D): {0}\n".format(round(D, precision)))
    f.write("\nЗначение статистики критерия (S): {0}\n".format(round(S, precision)))
    f.write("Критическое значение (S_alpha): {0}\n".format(round(S_alpha, precision)))
    if passed == True:
        f.write("Гипотеза не отвергается: S < S_alpha = {0} < {1}\n".format(round(S, precision), round(S_alpha, precision)))
    else:
        f.write("Гипотеза отвергается: S > S_alpha = {0} > {1}\n".format(round(S, precision), round(S_alpha, precision)))
    f.write("\nРезульт прохождения теста: {0}".format(passed))
    f.close()