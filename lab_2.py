import math
import scipy.stats as st


def generator(x0, n, a, b, c):
    x = [x0]
    for i in range(n):
        x.append((a * x[i]**2 + b * x[i] + c) % n)
    return x


def period(sequence):
    seq = list(reversed(sequence))
    max_len = len(seq) // 2 + 1
    for i in range(2, max_len):
        if seq[0:i] == seq[i:2*i]:
            return seq[0:i]
    return seq


def test_1(x, alpha=0.05):
    n = len(x)
    U = st.norm.ppf(1 - alpha / 2)
    Q = 0
    for i in range(n - 1): 
        if x[i] > x[i+1]:
            Q += 1
    return  Q - U * math.sqrt(n) / 2 <= n / 2 <= Q + U * math.sqrt(n) / 2


def calc_MX(x):
    return sum(x) / len(x)


def calc_DX(x):
    MX = calc_MX(x)
    return sum([(x - MX)**2 for x in x]) / (len(x) - 1)


def calc_frequencies(x, K, m):
    n = len(x)
    interval_hit = [0] * K
    for i in range(n):
        for j in range(K):
            if m / K * j <= x[i] < m / K * (j+1):
                interval_hit[j] += 1
    return [x/n for x in interval_hit]


def frequencies_test(x, K, alpha, m=1000):
    errors = []
    n = len(x)
    v = calc_frequencies(x, K, m)
    U = st.norm.ppf(1 - alpha / 2)
    for i in range(K):
        a = v[i] - U / K * math.sqrt(K - 1 / n) 
        b = v[i] + U / K * math.sqrt(K - 1 / n)
        if not (a <= 1 / K <= b): 
            errors.append(v[i])
    return errors == [], errors


def MX_estimate_test(MX, DX, n, alpha):
    U = st.norm.ppf(1 - alpha / 2)
    a = MX - U * math.sqrt(DX) / math.sqrt(n)
    b = MX + U * math.sqrt(DX) / math.sqrt(n) 
    return a <= n / 2 <= b


def DX_estimate_test(DX, n, alpha):
    a = (n - 1) * DX / st.chi2.isf(1 - alpha / 2, n)
    b = (n - 1) * DX / st.chi2.isf(alpha / 2, n)
    return a <= n**2 / 12 <= b


def test_2(x, K=20, alpha=0.05, m=1000):
    MX = calc_MX(x)
    DX = calc_DX(x)
    n = len(x)
    freq_pass, freq_errs = frequencies_test(x, K, alpha, m)
    MX_pass = MX_estimate_test(MX, DX, n, alpha)
    DX_pass = DX_estimate_test(DX, n, alpha)
    return freq_pass and MX_pass and DX_pass


def test_3(x, K=8, r=3):
    t = len(x) // r
    for i in range(r):
        if not (test_1(x[i * t:(i+1) * t]) and test_2(x[i * t:(i+1) * t], K)):
            return False
    return True


def sturgess_method(n):
    return math.floor(1 + math.log2(n))


def chi2_test(x, alpha=0.05, m=1000):
    n = len(x)
    K = sturgess_method(n)
    E = n / K
    v = calc_frequencies(x, K, m)
    S = n * sum([(O - E)**2 / E for O in v])
    return S < st.chi2.isf(alpha, K - 1)


def calc_D(x, m):
    n = len(x)
    D_plus = max([(i+1) / n - x[i] / m for i in range(n)])
    D_minus = max([x[i] / m - i / n for i in range(n)])
    return max(D_plus, D_minus)


def kolmogorov_test(x, alpha=0.05, m=1000):
    sort_x = sorted(x)
    D = calc_D(sort_x, m)
    n = len(sort_x)
    S = (6 * n * D + 1) / math.sqrt(n)
    return S < st.ksone.ppf(1 - alpha / 2, n) * math.sqrt(n)


def main():
    a = 100
    b = 1
    c = 2

    x0 = 1
    n = 1000

    x = generator(x0, n, a, b, c)
    T = period(x)

    result = test_1(T[:100])
    print(result)

    result_2 = test_2(T[:100])
    print(result_2)

    result_3 = test_3(T[:100])
    print(result_3)

    #result_chi2 = chi2_test(T[:100])
    #print(result_chi2)

    #result_kolm = kolmogorov_test(T[:100])
    #print(result_kolm)

    # period_max = 1
    # for a in range(130, 250):
    #     for b in range(1, 250):
    #         for c in range(1, 250):
    #             x = generator(x0, n, a, b, c)
    #             T = get_period(x)
    #             len_T = len(T)
    #             if len_T >= period_max and len_T != len(x):
    #                 period_max = len_T
    #                 print("LEN: ", len_T, "a: ", a, " | b: ", b, " | c: ", c)


if __name__ == "__main__":
    main()