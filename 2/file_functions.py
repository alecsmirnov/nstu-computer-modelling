import sys


def str_to_bool(str):
    return True if str == "True" else False


def read_generator_settings(filename):
    try:
        f = open(filename, "r")
    except IOError:
        print("Could not read file: ", filename)
        sys.exit()
    x0 = int(f.readline())
    a, b, c = [int(x) for x in f.readline().split()]
    n, m = [int(x) for x in f.readline().split()]
    f.close()
    return  x0, a, b, c, n, m


def read_tests_settings(filename):
    try:
        f = open(filename, "r")
    except IOError:
        print("Could not read file: ", filename)
        sys.exit()
    TESTS_COUNT = 5
    tests_data = [[] for i in range(TESTS_COUNT)]
    tests_data[0].append(float(f.readline()))
    data_temp = f.readline().split()
    tests_data[1].append(int(data_temp[0]))
    tests_data[1].append(float(data_temp[1]))
    tests_data[1].append(str_to_bool(data_temp[2]))
    data_temp = f.readline().split()
    tests_data[2].append(int(data_temp[0]))
    tests_data[2].append(int(data_temp[1]))
    tests_data[2].append(float(data_temp[2]))
    data_temp = f.readline().split()
    tests_data[3].append(float(data_temp[0]))
    tests_data[3].append(str_to_bool(data_temp[1]))
    tests_data[4].append(float(f.readline()))
    f.close()
    return  tests_data


def write_sequence(filename, seq):
    with open(filename, "w") as f:
        for value in seq:
            f.write("%s " % value)


def write_test1_results(filename, precision, alpha, n, Q, a, b, val, passed):
    f = open(filename, "w")
    f.write("alpha: {0}\n".format(alpha))
    f.write("n: {0}\n".format(n))
    f.write("Q: {0}\n".format(Q))
    f.write("confidence interval: [{0}; {1}]\n".format(round(a, precision), round(b, precision)))
    f.write("value: {0}\n".format(round(val, precision)))
    f.write("\ntest passed: {0}".format(passed))
    f.close()


def write_test2_results(filename, precision, alpha, n, m, K,
                       v, freq_pass, freq_errs, 
                       MX, MX_pass, MX_a, MX_b, MX_val, 
                       DX, DX_pass, DX_a, DX_b, DX_val, passed):
    f = open(filename, "w")
    f.write("alpha: {0}\n".format(alpha))
    f.write("n: {0}\n".format(n))
    f.write("m: {0}\n".format(m))
    f.write("K: {0}\n".format(K))
    f.write("v: {0}\n".format(str(v).strip('[]')))
    if freq_pass == False:
        f.write("frequencies test errors: {0}\n".format(str(v).strip('[]')))
    f.write("frequencies test passed: {0}\n".format(freq_pass))
    f.write("\nMX: {0}\n".format(round(MX, precision)))
    f.write("confidence interval: [{0}; {1}]\n".format(round(MX_a, precision), round(MX_b, precision)))
    f.write("value: {0}\n".format(round(MX_val, precision)))
    f.write("MX test passed: {0}\n".format(MX_pass))
    f.write("\nDX: {0}\n".format(round(DX, precision)))
    f.write("confidence interval: [{0}; {1}]\n".format(round(DX_a, precision), round(DX_b, precision)))
    f.write("value: {0}\n".format(round(DX_val, precision)))
    f.write("DX test passed: {0}\n".format(DX_pass))
    f.write("\ntest passed: {0}".format(passed))
    f.close()


def write_test3_results(filename, alpha, n, m, K, r, iters_info, passed):
    f = open(filename, "w")
    f.write("alpha: {0}\n".format(alpha))
    f.write("n: {0}\n".format(n))
    f.write("m: {0}\n".format(m))
    f.write("K: {0}\n".format(K))
    f.write("r: {0}\n".format(r))
    f.write("\ni\ttest1\ttest2:\n")
    for iter in iters_info:
        f.write("{0}\t{1}\t{2}\n".format(iter[0], iter[1], iter[2]))
    f.write("\ntest passed: {0}".format(passed))
    f.close()


def write_chi2_results(filename, precision, alpha, n, m, K, E, v, S, S_alpha, passed):
    f = open(filename, "w")
    f.write("alpha: {0}\n".format(alpha))
    f.write("n: {0}\n".format(n))
    f.write("m: {0}\n".format(m))
    f.write("K: {0}\n".format(K))
    f.write("\nE: {0}\n".format(round(E, precision)))
    f.write("O: {0}\n".format(str(v).strip('[]')))
    f.write("\nS: {0}\n".format(round(S, precision)))
    f.write("S_alpha: {0}\n".format(round(S_alpha, precision)))
    f.write("\ntest passed (S < S_alpha = {0} < {1}): {2}".format(round(S, precision), round(S_alpha, precision), passed))
    f.close()


def write_kolmogorov_results(filename, precision, alpha, n, m, D, S, S_alpha, passed):
    f = open(filename, "w")
    f.write("alpha: {0}\n".format(alpha))
    f.write("n: {0}\n".format(n))
    f.write("m: {0}\n".format(m))
    f.write("D: {0}\n".format(round(D, precision)))
    f.write("\nS: {0}\n".format(round(S, precision)))
    f.write("S_alpha: {0}\n".format(round(S_alpha, precision)))
    f.write("\ntest passed (S < S_alpha = {0} < {1}): {2}".format(round(S, precision), round(S_alpha, precision), passed))
    f.close()