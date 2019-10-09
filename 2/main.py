import generator as gr
import sequence_tests as tst
import random


# Названия файлов входных данных 
GENERATOR_FILENAME = tst.INPUT_PATH + "generator_settings.txt"
TESTS_FILENAME     = tst.INPUT_PATH + "tests_settings.txt"

# Названия файлов выходных данных
SEQUENCE_FILENAME        = tst.OUTPUT_PATH + "sequence.txt"
PERIOD_FILENAME          = tst.OUTPUT_PATH + "period.txt"
ANALYSIS_RESULT_FILENAME = tst.OUTPUT_PATH + "analysis_result.txt"


def main():
    x0, a, b, c, n, m = tst.ff.read_generator_settings(GENERATOR_FILENAME)
    x = gr.generator(x0, a, b, c, n, m)
    #x = [random.randrange(0, m) for x in range(n)]
    T = gr.period(x)
    T_len_min, tests_data = tst.ff.read_tests_settings(TESTS_FILENAME)
    tests_result = []
    # Проверка допустимой длины периода сгенерированной последовательности
    if T_len_min <= len(T):
        result_1 = tst.test1(T[:T_len_min], *tests_data[0])
        result_2 = tst.test2(T[:T_len_min], m, *tests_data[1])
        result_3 = tst.test3(T[:T_len_min], m, *tests_data[2])
        result_chi2 = tst.chi2_test(T[:T_len_min], m, *tests_data[3])
        result_kolm = tst.kolmogorov_test(T[:T_len_min], m, *tests_data[4])
        tests_result = [result_1, result_2, result_3, result_chi2, result_kolm]
        print("Тестирование завершено!\n")
    else:
        print("Период сгенерированной последовательности меньше чем {0}!\n".format(T_len_min))
    # Запись результатот тестирования в файлы
    tst.ff.write_analysis_result(ANALYSIS_RESULT_FILENAME, x0, a, b, c, n, m, T_len_min, tests_result)
    tst.ff.write_sequence(SEQUENCE_FILENAME, x)
    tst.ff.write_sequence(PERIOD_FILENAME, T)


if __name__ == "__main__":
    main()