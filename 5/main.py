import algorithms as alg
import file_functions as ff

INPUT_PATH  = "input/"
OUTPUT_PATH = "output/"

# Названия файла входных данных тестов
TESTS_FILENAME = INPUT_PATH + "tests_settings.txt"

# Названия файла выходных данных
TESTS_RESULT = OUTPUT_PATH + "tests_result.txt"

# Названия файлов выходных данных гистограмм/графиков
HISTOGRAM          = OUTPUT_PATH + "histogram.png"
DENSITY_CHART      = OUTPUT_PATH + "density_chart.png"
DISTRIBUTION_CHART = OUTPUT_PATH + "distribution_chart.png"


def main():
    # Чтение данных тестов
    n, mu, sigm, alpha, precision, histogram_run, charts_run = ff.read_tests_settings(TESTS_FILENAME)
    a, b = alg.get_bounds(mu, sigm)
    # Формирование последовательности
    sequence, density, count, modeling_time = alg.make_sequence(n, a, b, mu, sigm)
    # Формирование интервалов
    intervals, intervals_width = alg.get_intervals(sequence)
    hits, v = alg.interval_hits(sequence, intervals)
    # Тест критерия Хи-квадрат
    chi2_r, chi2_S, chi2_PSS, chi2_passed = alg.chi2_test(sequence, intervals, hits, mu, sigm, alpha)
    # Тест критерия Смирнова
    sm_S, sm_PSS, sm_passed = alg.smirnov_test(sequence, mu, sigm, alpha)
    ff.write_tests_results(TESTS_RESULT, precision, mu, sigm, alpha, a, b, sequence, density, count, 
                           intervals, hits, modeling_time,
                           chi2_r, chi2_S, chi2_PSS, chi2_passed, sm_S, sm_PSS, sm_passed)
    if charts_run:
        alg.make_charts(DENSITY_CHART, DISTRIBUTION_CHART, a, b, mu, sigm)
    if histogram_run:
        alg.make_histogram(HISTOGRAM, intervals, intervals_width, v, mu, sigm)


if __name__ == "__main__":
    main()