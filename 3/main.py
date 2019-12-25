import algorithms as alg
import file_functions as ff


INPUT_PATH  = "input/"
OUTPUT_PATH = "output/"

# Названия файла входных данных тестов
TESTS_FILENAME = "tests_settings.txt"

# Названия файлов выходных данных
RECURRENCE_FORMULA_RESULT = "recurrence_formula_result.txt"
POISSON_RESULT            = "poisson_result.txt"

# Названия файлов выходных данных гистограмм
RECURRENCE_FORMULA_HIST = "recurrence_formula_histogram.png"
POISSON_HIST            = "poisson_histogram.png"


def main():
    # Чтение данных тестов
    n, alpha, precision, recurrence_formula_run, m, p, poisson_run, lambd = ff.read_tests_settings(INPUT_PATH + TESTS_FILENAME)
    # Тест критерия типа хи-квадрат для Биномиального распределения
    if recurrence_formula_run:
        sequence, operations_count, P, implement_count = alg.recurrence_formula(n, m, p)
        S, S_alpha, PSS, v, interval_hits, PSS_passed, S_alpha_passed = alg.chi2_test(sequence, P, implement_count, alpha, plot=True, plot_name=OUTPUT_PATH+RECURRENCE_FORMULA_HIST) 
        ff.write_chi2_results(OUTPUT_PATH + RECURRENCE_FORMULA_RESULT, precision, sequence, P, alpha, n, m, p, ff.NONE, 
                              S, S_alpha, PSS, implement_count, v, interval_hits, operations_count, S_alpha_passed, PSS_passed)
    # Тест критерия типа хи-квадрат для распределения Пуассона
    if poisson_run:
        sequence, operations_count, P, implement_count = alg.poisson(n, lambd)
        S, S_alpha, PSS, v, interval_hits, PSS_passed, S_alpha_passed = alg.chi2_test(sequence, P, implement_count, alpha, plot=True, plot_name=OUTPUT_PATH+POISSON_HIST) 
        ff.write_chi2_results(OUTPUT_PATH + POISSON_RESULT, precision, sequence, P, alpha, n, ff.NONE, ff.NONE, lambd, 
                              S, S_alpha, PSS, implement_count, v, interval_hits, operations_count, S_alpha_passed, PSS_passed)


if __name__ == "__main__":
    main()