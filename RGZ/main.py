import algorithms as alg
import file_functions as ff


INPUT_PATH  = "input/"
OUTPUT_PATH = "output/"

# Названия файла входных данных тестов
TESTS_FILENAME = INPUT_PATH + "tests_settings.txt"

# Названия файла выходных данных
TESTS_RESULT = OUTPUT_PATH + "tests_result.txt"

# Названия файлов выходных данных гистограмм/графиков
HISTOGRAM = OUTPUT_PATH + "histogram.png"
CHART     = OUTPUT_PATH + "chart.png"


def main():
    # Чтение данных тестов
    n, mu, nu, alpha, precision, histogram_run, chart_run = ff.read_tests_settings(TESTS_FILENAME)
    # Формирование последовательности
    sequence, modeling_time = alg.make_sequence(n, mu, nu)
    # Формирование интервалов
    intervals = alg.get_intervals(sequence)
    hits, v = alg.interval_hits(sequence, intervals)
    # Тест критерия Хи-квадрат
    chi2_r, chi2_S, chi2_PSS, chi2_passed = alg.chi2_test(sequence, intervals, hits, mu, nu, alpha)
    # Тест критерия Крамера-Мизеса-Смирнов
    cms_S, cms_PSS, cms_passed = alg.cms_test(sequence, mu, v, alpha)
    ff.write_tests_results(TESTS_RESULT, precision, mu, nu, alpha, sequence, 
                           intervals, hits, modeling_time,
                           chi2_r, chi2_S, chi2_PSS, chi2_passed, cms_S, cms_PSS, cms_passed)
    if chart_run:
        alg.make_chart(CHART, mu, nu)
    if histogram_run:
        alg.make_histogram(HISTOGRAM, intervals, v, mu, nu)


if __name__ == "__main__":
    main()