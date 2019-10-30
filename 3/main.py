import algorithms as alg


def main():
    n = 40
    m = 5
    p = [0.2, 0.5, 0.8]
    lamb = 14
    alpha = 0.05

    sequence, operations_count, P = alg.poisson_alg(n, lamb)

    result_chi2 = alg.chi2_test(sequence, P, alpha, plot=True) 
    print(result_chi2)


if __name__ == "__main__":
    main()