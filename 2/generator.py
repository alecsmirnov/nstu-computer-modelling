def generator(x0, a, b, c, n, m):
    x = [x0]
    for i in range(n):
        x.append((a * x[i]**2 + b * x[i] + c) % m)
    return x


def period(sequence):
    seq = list(reversed(sequence))
    max_len = len(seq) // 2 + 1
    for i in range(2, max_len):
        if seq[0:i] == seq[i:2*i]:
            return seq[0:i]
    return seq