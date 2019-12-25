import algorithms as alg
import file_functions as ff


INPUT_PATH  = "input/"
OUTPUT_PATH = "output/"

# Названия файла входных данных тестов
TESTS_FILENAME = "tests_settings.txt"

# Названия файла выходных данных
TESTS_RESULT = "tests_result.txt"

# Названия файлов выходных данных гистограмм/графиков
HISTOGRAM          = "histogram.png"
DENSITY_CHART      = "density_chart.png"
DISTRIBUTION_CHART = "distribution_chart.png"


def main():
    # Чтение данных тестов
    n, sigm, alpha, precision, histogram_run, charts_run = ff.read_tests_settings(INPUT_PATH + TESTS_FILENAME)
    # Формирование последовательности
    sequence, modeling_time = alg.make_sequence(n, sigm)
    # Формирование интервалов
    intervals = alg.get_intervals(sequence)
    hits, v = alg.interval_hits(sequence, intervals)
    # Тест критерия типа Хи-квадрат
    chi2_r, chi2_S, chi2_PSS, chi2_passed = alg.chi2_test(sequence, intervals, hits, sigm, alpha)
    # Тест критерия типа Омега-квадрат Андерса-Дарлинга
    ad_S, ad_PSS, ad_passed = alg.anderson_darling_test(sequence, sigm, alpha)
    ff.write_tests_results(OUTPUT_PATH + TESTS_RESULT, precision, sigm, alpha, sequence, intervals, hits, modeling_time,
                           chi2_r, chi2_S, chi2_PSS, chi2_passed, ad_S, ad_PSS, ad_passed)
    if histogram_run:
        alg.make_histogram(OUTPUT_PATH + HISTOGRAM, intervals, v, sigm)
    if charts_run:
        alg.make_charts(OUTPUT_PATH + DENSITY_CHART, OUTPUT_PATH + DISTRIBUTION_CHART, sigm)


if __name__ == "__main__":
    main()