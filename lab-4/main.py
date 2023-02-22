import numpy as np
eps = 1e-4

k = int(input())

lambdas = list(map(float, input().split()))

alpha = float(input())

n = int(input())

y_to_xs = {}
y_freq = [0] * k
words = set()

for i in range(k):
    y_to_xs[i] = {}

for i in range(n):
    line = input().split()
    y = int(line[0]) - 1
    x = set(line[2::])
    y_freq[y] += 1
    for word in x:
        y_to_xs[y][word] = y_to_xs[y].get(word, 0) + 1
        words.add(word)

m = int(input())

x_test = [0] * m

for i in range(m):
    line = input().split()
    x_test[i] = set(line[1::])

p = [0] * k

for y in range(k):
    denominator = y_freq[y] + 2 * alpha
    prob = [0] * len(words)
    i = 0
    for word in words:
        prob[i] = (y_to_xs[y].get(word, 0) + alpha) / denominator
        i += 1
    p[y] = prob

for x in x_test:
    values = [0] * k
    for y in range(k):
        p_xy = 0
        i = 0
        for word in words:
            if word in x:
                p_xy += np.log(p[y][i])
            else:
                p_xy += np.log(1 - p[y][i])
            i += 1
        values[y] = np.log(lambdas[y]) + np.log(y_freq[y] / n) + p_xy
    sm = 0
    max_ln = max(values)
    for y in range(k):
        if abs(values[y]) <= eps:
            values[y] = 0
            continue
        values[y] = np.exp(values[y] - max_ln)
        sm += values[y]

    for y in range(k):
        values[y] /= sm

    print(*values, sep=" ")
