import sys


# Перевод стокового логического значения в булевое
def str_to_bool(str):
    return True if str == "True" else False


# Чтение данных для генератора псевдослучайных чисел
def read_generator_settings(filename):
    try:
        f = open(filename, "r")
    except IOError:
        print("Could not read file: ", filename)
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
        print("Could not read file: ", filename)
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
        f.write("Sequence with parameters:\n")
        f.write("x0: {0}\n".format(x0))
        f.write("a: {0}\n".format(a))
        f.write("b: {0}\n".format(b))
        f.write("c: {0}\n".format(c))
        f.write("n: {0}\n".format(n))
        f.write("m: {0}\n".format(n))
        f.write("period len: {0}\n".format(T_len))
        if tests_result != []:
            f.write("\nTests result:\n")
            f.write("test 1: {0}\n".format(tests_result[0]))
            f.write("test 2: {0}\n".format(tests_result[1]))
            f.write("test 3: {0}\n".format(tests_result[2]))
            f.write("chi2 test: {0}\n".format(tests_result[3]))
            f.write("kolmogorov test: {0}\n".format(tests_result[4]))
        else:
            f.write("\nPeriod of the generated sequence is less than {0}!\n".format(T_len))


# Записать в файл результаты теста 1
def write_test1_results(filename, precision, alpha, n, Q, a, b, val, passed):
    f = open(filename, "w")
    # Уровень значимости
    f.write("alpha: {0}\n".format(alpha))
    # Количество элементов последовательности
    f.write("n: {0}\n".format(n))
    # Количество перестановок
    f.write("Q: {0}\n".format(Q))
    # Доверительный интервал
    f.write("confidence interval: [{0}; {1}]\n".format(round(a, precision), round(b, precision)))
    # Значение попадающее (или нет) в доверительный интервал
    f.write("value: {0}\n".format(round(val, precision)))
    f.write("\ntest passed: {0}".format(passed))
    f.close()


# Записать в файл результаты теста 2
def write_test2_results(filename, precision, alpha, n, m, K,
                       v, freq_pass, freq_errs, 
                       MX, MX_pass, MX_a, MX_b, MX_val, 
                       DX, DX_pass, DX_a, DX_b, DX_val, passed):
    f = open(filename, "w")
    # Уровень значимости
    f.write("alpha: {0}\n".format(alpha))
    # Количество элементов последовательности
    f.write("n: {0}\n".format(n))
    # Основание последовательности
    f.write("m: {0}\n".format(m))
    # Количество интервалов разбиваемой последовательности
    f.write("K: {0}\n".format(K))
    # Относительные частоты попадания в интервал
    f.write("v: {0}\n".format(str(v).strip('[]')))
    # В случае провала теста -- вывод ошибок: вероятностей не попавших в интервал
    if freq_pass == False:
        f.write("frequencies test errors: {0}\n".format(str(v).strip('[]')))
    # Результат прохождения частотного теста
    f.write("frequencies test passed: {0}\n".format(freq_pass))
    f.write("\nMX: {0}\n".format(round(MX, precision)))
    # Доверительный интервал
    f.write("confidence interval: [{0}; {1}]\n".format(round(MX_a, precision), round(MX_b, precision)))
    f.write("value: {0}\n".format(round(MX_val, precision)))
    # Результат оценки сходимости математического ожидания
    f.write("MX test passed: {0}\n".format(MX_pass))
    f.write("\nDX: {0}\n".format(round(DX, precision)))
    # Доверительный интервал
    f.write("confidence interval: [{0}; {1}]\n".format(round(DX_a, precision), round(DX_b, precision)))
    f.write("value: {0}\n".format(round(DX_val, precision)))
    # Результат оценки сходимости дисперсии
    f.write("DX test passed: {0}\n".format(DX_pass))
    f.write("\ntest passed: {0}".format(passed))
    f.close()


# Записать в файл результаты теста 3
def write_test3_results(filename, alpha, n, m, K, r, iters_info, passed):
    f = open(filename, "w")
    # Уровень значимости
    f.write("alpha: {0}\n".format(alpha))
    # Количество элементов последовательности
    f.write("n: {0}\n".format(n))
    # Основание последовательности
    f.write("m: {0}\n".format(m))
    # Количество интервалов разбиваемой последовательности
    f.write("K: {0}\n".format(K))
    # Количество подпоследовательностей данной последовательности
    f.write("r: {0}\n".format(r))
    # Результаты прохождения тестов на каждой подпоследовательности (итерации)
    f.write("\ni\ttest1\ttest2:\n")
    for iter in iters_info:
        f.write("{0}\t{1}\t{2}\n".format(iter[0], iter[1], iter[2]))
    f.write("\ntest passed: {0}".format(passed))
    f.close()


# Записать в файл результаты хи-квадрат теста
def write_chi2_results(filename, precision, alpha, n, m, K, E, v, S, S_alpha, passed):
    f = open(filename, "w")
    # Уровень значимости
    f.write("alpha: {0}\n".format(alpha))
    # Количество элементов последовательности
    f.write("n: {0}\n".format(n))
    # Основание последовательности
    f.write("m: {0}\n".format(m))
    # Количество интервалов разбиваемой последовательности
    f.write("K: {0}\n".format(K))
    # Теоретическая вероятность попадания в интервал
    f.write("\nE: {0}\n".format(round(E, precision)))
    # Относительные частоты попадания в интервал
    f.write("O: {0}\n".format(str(v).strip('[]')))
    # Значение статистики критерия
    f.write("\nS: {0}\n".format(round(S, precision)))
    # Критическое значение 
    f.write("S_alpha: {0}\n".format(round(S_alpha, precision)))
    f.write("\ntest passed (S < S_alpha = {0} < {1}): {2}".format(round(S, precision), round(S_alpha, precision), passed))
    f.close()


# Записать в файл результаты теста Колмогорова
def write_kolmogorov_results(filename, precision, alpha, n, m, D, S, S_alpha, passed):
    f = open(filename, "w")
    # Уровень значимости
    f.write("alpha: {0}\n".format(alpha))
    # Количество элементов последовательности
    f.write("n: {0}\n".format(n))
    # Основание последовательности
    f.write("m: {0}\n".format(m))
    f.write("D: {0}\n".format(round(D, precision)))
    # Значение статистики критерия
    f.write("\nS: {0}\n".format(round(S, precision)))
    # Критическое значение 
    f.write("S_alpha: {0}\n".format(round(S_alpha, precision)))
    f.write("\ntest passed (S < S_alpha = {0} < {1}): {2}".format(round(S, precision), round(S_alpha, precision), passed))
    f.close()