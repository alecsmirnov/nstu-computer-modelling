import generator as gr
import sequence_tests as tst

T_LEN = 100


def main():
    x0, a, b, c, n, m = tst.ff.read_generator_settings(tst.INPUT_PATH + "generator_settings.txt")

    x = gr.generator(x0, a, b, c, n, m)
    T = gr.period(x)

    tst.ff.write_sequence(tst.OUTPUT_PATH + "sequence.txt", x)
    tst.ff.write_sequence(tst.OUTPUT_PATH + "period.txt", T)

    if T_LEN <= len(T):
        tests_data = tst.ff.read_tests_settings(tst.INPUT_PATH + "tests_settings.txt")

        result_1 = tst.test1(T[:T_LEN], *tests_data[0])
        result_2 = tst.test2(T[:T_LEN], m, *tests_data[1])
        result_3 = tst.test3(T[:T_LEN], m, *tests_data[2])
        result_chi2 = tst.chi2_test(T[:T_LEN], m, *tests_data[3])
        result_kolm = tst.kolmogorov_test(T[:T_LEN], m, *tests_data[4])

        print("test 1:          ", result_1)
        print("test 2:          ", result_2)
        print("test 3:          ", result_3)
        print("chi2 test:       ", result_chi2)
        print("kolmogorov test: ", result_kolm)
    else:
        print("Period of the generated sequence is less than {0}!\n".format(T_LEN))


if __name__ == "__main__":
    main()