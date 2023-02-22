from math import log2


class Leaf:
    def __init__(self, y):
        self.y = y
        self.w = 1


class Node:
    def __init__(self, j, bj):
        self.j = j
        self.bj = bj
        self.left_child = None
        self.right_child = None
        self.w = 1


m, k, h = map(int, input().split())

n = int(input())

x_train = [0] * n
y_train = [0] * n

for i in range(n):
    features = list(map(int, input().split()))
    x_train[i] = features[:-1]
    y_train[i] = features[-1] - 1


def build_tree(xs, ys, h):
    cnt_ys = 0
    freq = [0] * k
    log_sum = 0
    for i in range(len(ys)):
        freq[ys[i]] += 1

    major_freq = -1
    major = -1
    for y in range(k):
        if freq[y] > 0:
            log_sum += freq[y] * log2(freq[y])
            cnt_ys += 1
        if freq[y] > major_freq:
            major_freq = freq[y]
            major = y

    if cnt_ys <= 1 or h == 0:
        return Leaf(major)

    max_gain = (log_sum - log2(len(xs)) * len(xs)) / len(xs)
    best_j = 0
    best_bj = max(list(map(lambda feature: feature[0], xs))) + 1
    for j in range(m):
        pairs = [0] * len(xs)
        for i in range(len(xs)):
            pairs[i] = (xs[i][j], i)
        pairs.sort(key=lambda pr: pr[0])

        freq_prefix = [0] * k
        prefix_log_sum = 0
        suffix_log_sum = log_sum
        prefix_sum = 0
        suffix_sum = len(ys)

        for i in range(len(pairs)):
            border, ind = pairs[i]
            y = ys[ind]

            if i == 0 or border != pairs[i - 1][0]:
                phi_prefix = 0
                if i > 0:
                    phi_prefix = (prefix_log_sum - log2(i) * prefix_sum) / i

                phi_suffix = 0
                if len(xs) - i > 0:
                    phi_suffix = (suffix_log_sum - log2(len(xs) - i) * suffix_sum) / (len(xs) - i)

                gain = i / len(xs) * phi_prefix + (len(xs) - i) / len(xs) * phi_suffix
                if gain > max_gain:
                    max_gain = gain
                    best_j = j
                    best_bj = border

            if freq_prefix[y] > 0:
                prefix_log_sum -= freq_prefix[y] * log2(freq_prefix[y])
            suffix_log_sum -= (freq[y] - freq_prefix[y]) * log2(freq[y] - freq_prefix[y])
            freq_prefix[y] += 1
            prefix_log_sum += freq_prefix[y] * log2(freq_prefix[y])
            prefix_sum += 1
            if freq[y] - freq_prefix[y] > 0:
                suffix_log_sum += (freq[y] - freq_prefix[y]) * log2(freq[y] - freq_prefix[y])
            suffix_sum -= 1

    left_xs = []
    left_ys = []
    right_xs = []
    right_ys = []
    for i in range(len(xs)):
        if xs[i][best_j] < best_bj:
            left_xs.append(xs[i])
            left_ys.append(ys[i])
        else:
            right_xs.append(xs[i])
            right_ys.append(ys[i])

    if len(left_xs) == 0 or len(right_xs) == 0:
        return Leaf(major)

    node = Node(best_j, best_bj)

    left_child = build_tree(left_xs, left_ys, h - 1)
    right_child = build_tree(right_xs, right_ys, h - 1)

    node.left_child = left_child
    node.right_child = right_child
    node.w = left_child.w + right_child.w + 1

    return node


def dfs(node, ind):
    if isinstance(node, Node):
        print(f"Q {node.j + 1} {node.bj} {ind + 1} {ind + node.left_child.w + 1}")
        dfs(node.left_child, ind + 1)
        dfs(node.right_child, ind + node.left_child.w + 1)
    if isinstance(node, Leaf):
        print(f"C {node.y + 1}")


root = build_tree(x_train, y_train, h)

print(root.w)

dfs(root, 1)
