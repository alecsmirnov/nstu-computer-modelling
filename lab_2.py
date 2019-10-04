import math
import scipy.stats as st
import matplotlib.pyplot as plt


def generator(x0, n, a, b, c):
    x = [x0]
    for i in range(n):
        x.append((a * x[i]**2 + b * x[i] + c) % n)
    return x


def get_period(sequence):
    seq = list(reversed(sequence))
    max_len = len(seq) // 2 + 1
    for i in range(2, max_len):
        if seq[0:i] == seq[i:2*i]:
            return seq[0:i]
    return seq


def draw_chart(x, K):
    gfig, gax = plt.subplots()
    gn, gbins, gpatches = gax.hist(x, K, density=1)
    gax.set_title("Гистограмма частот (n = " + str(len(x)) + ")") 
    gfig.tight_layout() 
    plt.show()


def test_1(x, alpha=0.05):
    U = st.norm.ppf(1 - alpha / 2)
    Q = 0
    n = len(x)
    for i in range(n - 1): 
        if x[i] > x[i+1]:
            Q += 1
    return n / 2 < Q + U * math.sqrt(n) / 2 and Q - U * math.sqrt(n) / 2 < n / 2 


def calc_MX(x):
    return sum(x) / len(x)


def calc_DX(x):
    MX = calc_MX(x)
    return sum([(x - MX)**2 for x in x]) / (len(x) - 1)


def calc_frequencies(x, K):
    n = len(x)
    interval_hit = [0] * K
    for i in range(n):
        for j in range(K):
            if n / K * j <= x[i] <= n / K * (j+1):
                interval_hit[j] += 1
    return [x/n for x in interval_hit]


def frequencies_test(x, K, alpha):
    errors = []
    v = calc_frequencies(x, K)
    U = st.norm.ppf(1 - alpha / 2)
    n = len(x)
    for i in range(K):
        a = v[i] - U / K * math.sqrt(K - 1 / n) 
        b = v[i] + U / K * math.sqrt(K - 1 / n)
        if 1 / K < a and b < 1 / K: 
            errors.append(v[i])
    return errors == [], errors


def MX_estimate_test(MX, DX, n, alpha):
    U = st.norm.ppf(1 - alpha / 2)
    a = MX - U * math.sqrt(DX) / math.sqrt(n)
    b = MX + U * math.sqrt(DX) / math.sqrt(n) 
    return not (n / 2 < a and b < n / 2)


def DX_estimate_test(DX, n, alpha):
    a = (n - 1) * DX / st.chi2.isf(1 - alpha / 2, n)
    b = (n - 1) * DX / st.chi2.isf(alpha / 2, n)
    return not (n**2 / 12 < a and b < n**2 / 12)


def test_2(x, K=20, alpha=0.05):
    MX = calc_MX(x)
    DX = calc_DX(x)
    n = len(x)
    freq_pass = frequencies_test(x, K, alpha)
    MX_pass = MX_estimate_test(MX, DX, n, alpha)
    DX_pass = DX_estimate_test(DX, n, alpha)
    return freq_pass and MX_pass and DX_pass


def main():
    a = 100
    b = 1
    c = 2

    x0 = 1
    n = 1000

    x = generator(x0, n, a, b, c)
    #T = get_period(x)
    #print(T, len(T))

    #result = test_1(x[:100])
    #print(result)

    result_2 = test_2(x[:100])
    print(result_2)

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