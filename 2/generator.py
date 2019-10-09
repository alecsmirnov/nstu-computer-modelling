# Генератор псевдослучайно последовательности
def generator(x0, a, b, c, n, m):
    x = [x0]
    for i in range(n):
        x.append((a * x[i]**2 + b * x[i] + c) % m)
    return x


# Выделение периода последовательности с отбрасыванием предпериода
def period(sequence):
    # Инвертируем последовательность
    seq = list(reversed(sequence))
    # Проверяем подпоследовательности до середины последовательности
    max_len = len(seq) // 2 + 1
    # Увеличиваем длину подпоследовательности и проверяем на равенство соседнюю за ней
    for i in range(2, max_len):
        if seq[0:i] == seq[i:2*i]:
            return seq[0:i]
    return seq