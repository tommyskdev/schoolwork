import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))

    adj = [[] for _ in range(n + 1)]
    total = 0
    for _ in range(n - 1):
        a = int(next(it))
        b = int(next(it))
        e = int(next(it))
        adj[a].append((b, e))
        adj[b].append((a, e))
        total += e

    if n == 1:
        sys.stdout.write("0\n")
        return

    parent = [0] * (n + 1)
    pw = [0] * (n + 1)
    order = []
    stack = [1]
    parent[1] = -1
    while stack:
        v = stack.pop()
        order.append(v)
        for u, w in adj[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            pw[u] = w
            stack.append(u)

    down = [0] * (n + 1)
    best = 0

    for v in reversed(order):
        first = 0
        second = 0
        for u, w in adj[v]:
            if u == parent[v]:
                continue
            val = w + down[u]
            if val < first:
                second = first
                first = val
            elif val < second:
                second = val
        cand = first + second
        if cand < best:
            best = cand
        down[v] = first if first < 0 else 0

    sys.stdout.write(str(total - 2 * best) + "\n")

if __name__ == "__main__":
    main()
