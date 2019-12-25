import algorithms as alg
import file_functions as ff


# Директории для входных и выходных данных
INPUT_PATH  = "input/"
OUTPUT_PATH = "output/"

# Названия файлов входных данных 
GENERATOR_FILENAME = "generator_settings.txt"
TESTS_FILENAME     = "tests_settings.txt"

# Названия файлов выходных данных
SEQUENCE_FILENAME        = "sequence.txt"
PERIOD_FILENAME          = "period.txt"
ANALYSIS_RESULT_FILENAME = "analysis_result.txt"

TEST2_HISTOGRAM     = "test2_histogram.png"
CHI2_TEST_HISTOGRAM = "chi2_test_histogram.png"

# Количество тестов
TESTS_COUNT = 5


# Чтение данных для генератора псевдослучайных чисел
def read_generator_settings(filename):
    try:
        f = open(filename, "r")
    except IOError:
        print("Невозможно открыть файл: ", filename)
        ff.exit()
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
        exit()
    tests_data = [[] for i in range(TESTS_COUNT)]
    # Получаем длину допустимого периода последовательности
    T_len_min = int(f.readline())
    # Данные для теста 2: K
    tests_data[1].append(int(f.readline()))
    # Данные для теста 3: К, r
    data_temp = f.readline().split()
    tests_data[2].append(int(data_temp[0]))
    tests_data[2].append(int(data_temp[1]))
    alpha = float(f.readline())
    precision = int(f.readline())
    f.close()
    return  T_len_min, tests_data, alpha, precision


def main():
    x0, a, b, c, n, m = read_generator_settings(INPUT_PATH + GENERATOR_FILENAME)
    x = alg.generator(x0, a, b, c, n, m)
    T = alg.period(x)
    T_len_min, tests_data, alpha, precision = read_tests_settings(INPUT_PATH + TESTS_FILENAME)
    # Параметры для тестов
    TESTS_FUNC      = [alg.test1, alg.test2, alg.test3, alg.chi2_test, alg.kolmogorov_test]
    TESTS_RES_FUNC  = [ff.write_test1_results, ff.write_test2_results, ff.write_test3_results, ff.write_chi2_results, ff.write_kolmogorov_results]
    TESTS_RES_FILES = ["test1_result.txt", "test2_result.txt", "test3_result.txt", "chi2_test_result.txt", "kolmogorov_test_result.txt"]
    # Проверка допустимой длины периода сгенерированной последовательности
    if T_len_min <= len(T):
        tests_passed = []
        for i in range(TESTS_COUNT):
            test_result = TESTS_FUNC[i](T[:T_len_min], m, *tests_data[i], alpha)
            TESTS_RES_FUNC[i](OUTPUT_PATH + TESTS_RES_FILES[i], precision, alpha, *test_result)
            tests_passed.append(test_result[-1])
            if i == 1:
                ff.draw_histogram(OUTPUT_PATH + TEST2_HISTOGRAM, test_result[3], test_result[0], test_result[1])
            if i == 3:
                ff.draw_histogram(OUTPUT_PATH + CHI2_TEST_HISTOGRAM, test_result[4], test_result[0], test_result[1])
        ff.write_analysis_result(OUTPUT_PATH + ANALYSIS_RESULT_FILENAME, x0, a, b, c, n, m, len(T), T_len_min, tests_passed)
        print("Тестирование завершено!\n")
    else:
        print("Период сгенерированной последовательности меньше чем {0}!\n".format(T_len_min))
    ff.write_sequence(OUTPUT_PATH + SEQUENCE_FILENAME, x)
    ff.write_sequence(OUTPUT_PATH + PERIOD_FILENAME, T)


if __name__ == "__main__":
    main()