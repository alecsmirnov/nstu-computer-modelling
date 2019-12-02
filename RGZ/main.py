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
    #'''  
    empiric_distr = alg.chi2_distribution
    theor_distr = alg.chi2.cdf
    k = 12
    # Чтение данных тестов
    n, mu, nu, alpha, precision, histogram_run, chart_run = ff.read_tests_settings(TESTS_FILENAME)
    # Формирование последовательности
    sequence, modeling_time = alg.make_sequence(n, empiric_distr, k)
    # Формирование интервалов
    intervals, intervals_width = alg.get_intervals(sequence)
    hits, v = alg.interval_hits(sequence, intervals)
    # Тест критерия Хи-квадрат
    chi2_r, chi2_S, chi2_PSS, chi2_passed = alg.chi2_test(n, intervals, hits, alpha, theor_distr, k)
    # Тест критерия Крамера-Мизеса-Смирнов
    cms_S, cms_PSS, cms_passed = alg.cms_test(sequence, alpha, theor_distr, k)
    ff.write_tests_results(TESTS_RESULT, precision, mu, nu, alpha, sequence, 
                           intervals, hits, modeling_time,
                           chi2_r, chi2_S, chi2_PSS, chi2_passed, cms_S, cms_PSS, cms_passed)
    if chart_run:
        alg.make_chart(CHART, "Функция распределения Хи-квадрат", theor_distr, k)
    if histogram_run:
        alg.make_histogram(HISTOGRAM, intervals, intervals_width, v, theor_distr, k)
    '''
    empiric_distr = alg.fisher_distribution
    theor_distr = alg.f.cdf
    # Чтение данных тестов
    n, mu, nu, alpha, precision, histogram_run, chart_run = ff.read_tests_settings(TESTS_FILENAME)
    # Формирование последовательности
    sequence, modeling_time = alg.make_sequence(n, empiric_distr, mu, nu)
    # Формирование интервалов
    intervals, intervals_width = alg.get_intervals(sequence)
    hits, v = alg.interval_hits(sequence, intervals)
    # Тест критерия Хи-квадрат
    chi2_r, chi2_S, chi2_PSS, chi2_passed = alg.chi2_test(n, intervals, hits, alpha, theor_distr, mu, nu)
    # Тест критерия Крамера-Мизеса-Смирнов
    cms_S, cms_PSS, cms_passed = alg.cms_test(sequence, alpha, theor_distr, mu, nu)
    ff.write_tests_results(TESTS_RESULT, precision, mu, nu, alpha, sequence, 
                           intervals, hits, modeling_time,
                           chi2_r, chi2_S, chi2_PSS, chi2_passed, cms_S, cms_PSS, cms_passed)
    if chart_run:
        alg.make_chart(CHART, "Функция распределения Фишера", theor_distr, mu, nu)
    if histogram_run:
        alg.make_histogram(HISTOGRAM, intervals, intervals_width, v, theor_distr, mu, nu)
    '''     


if __name__ == "__main__":
    main()