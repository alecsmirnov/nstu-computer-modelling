import algorithms as alg


def main():
    n = 50
    sigm = 1.5
    alpha = 0.05
    sequence = alg.make_sequence(n, sigm)
    intervals = alg.get_intervals(sequence)
    hits, v = alg.interval_hits(sequence, intervals)
    #make_histogram("histogram.png", intervals, v, sigm)

    chi2_res = alg.chi2_test(sequence, intervals, hits, sigm, alpha)
    print(chi2_res)
    
    ad_res = alg.anderson_darling_test(sequence, sigm, alpha)
    print(ad_res)


if __name__ == "__main__":
    main()