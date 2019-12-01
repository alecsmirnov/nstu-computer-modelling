import algorithms as alg

import sys
import numpy as np
import matplotlib.pyplot as plt

import scipy.stats as stats


def draw_chart(picturename, title, x_label, y_label, func, *arg):
    X_MAX = 10
    X_STEP = 0.005
    x = np.arange(0, X_MAX + X_STEP, X_STEP) 
    plt.xticks(range(0, X_MAX + 1))
    plt.title(title)
    plt.xlabel(x_label) 
    plt.ylabel(y_label)
    y = [func(x, *arg) for x in x]
    plt.plot(x, y)
    plt.grid(True)
    plt.savefig(picturename)
    plt.clf()


def draw_histogram(picturename, intervals, v, theor_intervals, theor_v, bar_width):
    plt.xlabel("Интервалы")
    plt.ylabel("Частоты")
    plt.xticks(intervals, rotation=90)
    plt.plot(theor_intervals, theor_v, marker="o")
    plt.bar(intervals[:len(intervals) - 1], v, width=bar_width, alpha=0.5, 
            align="edge", edgecolor="grey", color="lightgrey")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(picturename)
    plt.clf()   


# Сформировать гистограмму теоретической и эмпирической функции плотности распределения
def make_histogram(picturename, intervals, v, mu, nu):
    theor_intervals = []
    theor_v = []
    bar_width = intervals[-1] / (len(intervals) - 1)
    for i in range(len(intervals)):
        theor_intervals.append(i * bar_width + bar_width / 2)
        theor_v.append(stats.f.cdf((i + 1) * bar_width, mu, nu) - stats.f.cdf(i * bar_width, mu, nu))
    draw_histogram(picturename, intervals, v, theor_intervals, theor_v, bar_width)



def main():
    alpha = 0.05
    n = 1000
    mu = 4
    nu = 2
    sequence, modeling_time = alg.make_sequence(n, mu, nu)
    intervals = alg.get_intervals(sequence)
    hits, v = alg.interval_hits(sequence, intervals)
    make_histogram("hist.png", intervals, v, mu, nu)
    r, S, PSS, passed = alg.chi2_test(sequence, intervals, hits, mu, nu, alpha)
    print(r, S, PSS, passed)
    S, PSS, passed = alg.cms_test(sequence, mu, v, alpha)
    print(S, PSS, passed)


if __name__ == "__main__":
    main()