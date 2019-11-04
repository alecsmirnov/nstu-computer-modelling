import algorithms as alg

NONE = 0

INPUT_PATH  = "input/"
OUTPUT_PATH = "output/"

TESTS_FILENAME = INPUT_PATH + "tests_settings.txt"

RECURRENCE_FORMULAS_RESULT = OUTPUT_PATH + "recurrence_formulas_test_result.txt"
POISSON_RESULT             = OUTPUT_PATH + "poisson_test_result.txt"

RECURRENCE_FORMULAS_HIST = OUTPUT_PATH + "recurrence_formulas_histogram.png"
POISSON_HIST             = OUTPUT_PATH + "poisson_histogram.png"


def main():
    n, m, p, lambd, alpha, precision = alg.ff.read_tests_settings(TESTS_FILENAME)

    #p = [0.2, 0.5, 0.8]

    sequence, operations_count, P = alg.recurrence_formulas_alg(n, m, p)
    S_alpha, implement_count, v, interval_hits, passed = alg.chi2_test(sequence, P, alpha, plot=True, plot_name=RECURRENCE_FORMULAS_HIST) 
    alg.ff.write_chi2_results(RECURRENCE_FORMULAS_RESULT, precision, sequence, P, alpha, n, m, p, NONE, 
                              S_alpha, implement_count, v, interval_hits, operations_count, passed)

    sequence, operations_count, P = alg.poisson_alg(n, lambd)
    S_alpha, implement_count, v, interval_hits, passed = alg.chi2_test(sequence, P, alpha, plot=True, plot_name=POISSON_HIST) 
    alg.ff.write_chi2_results(POISSON_RESULT, precision, sequence, P, alpha, n, NONE, NONE, lambd, 
                              S_alpha, implement_count, v, interval_hits, operations_count, passed)

if __name__ == "__main__":
    main()