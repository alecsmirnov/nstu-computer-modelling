import algorithms as alg

INPUT_PATH  = "input/"
OUTPUT_PATH = "output/"

# Названия файла входных данных тестов
TESTS_FILENAME = INPUT_PATH + "tests_settings.txt"

# Названия файлов выходных данных
RECURRENCE_FORMULA_RESULT = OUTPUT_PATH + "recurrence_formula_result.txt"
POISSON_RESULT            = OUTPUT_PATH + "poisson_result.txt"

# Названия файлов выходных данных гистограмм
RECURRENCE_FORMULA_HIST = OUTPUT_PATH + "recurrence_formula_histogram.png"
POISSON_HIST            = OUTPUT_PATH + "poisson_histogram.png"


def main():
    # Чтение данных тестов
    n, m, p, lambd, alpha, precision = alg.ff.read_tests_settings(TESTS_FILENAME)
    # Тест критерия типа хи-квадрат для Биномиального распределения
    sequence, operations_count, P, implement_count = alg.recurrence_formula(n, m, p)
    S, S_alpha, v, interval_hits, passed = alg.chi2_test(sequence, P, implement_count, alpha, plot=True, plot_name=RECURRENCE_FORMULA_HIST) 
    alg.ff.write_chi2_results(RECURRENCE_FORMULA_RESULT, precision, sequence, P, alpha, n, m, p, alg.ff.NONE, 
                              S, S_alpha, implement_count, v, interval_hits, operations_count, passed)
    # Тест критерия типа хи-квадрат для распределения Пуассона
    sequence, operations_count, P, implement_count = alg.poisson(n, lambd)
    S, S_alpha, v, interval_hits, passed = alg.chi2_test(sequence, P, implement_count, alpha, plot=True, plot_name=POISSON_HIST) 
    alg.ff.write_chi2_results(POISSON_RESULT, precision, sequence, P, alpha, n, alg.ff.NONE, alg.ff.NONE, lambd, 
                              S, S_alpha, implement_count, v, interval_hits, operations_count, passed)


if __name__ == "__main__":
    main()