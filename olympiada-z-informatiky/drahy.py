import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    k = int(next(it))

    N = 2 * n
    adj = [[] for _ in range(N)]

    for _ in range(m):
        x = int(next(it)) - 1
        y = int(next(it)) - 1
        d = int(next(it))
        adj[x].append((y, d))
        adj[y].append((x, d))
        adj[n + x].append((n + y, 0))

    for v in range(n):
        adj[v].append((n + v, k))
        adj[n + v].append((v, 0))

    INF = float("inf")
    dist = [INF] * N
    dist[0] = 0
    heap = [(0, 0)]
    while heap:
        d0, v = heapq.heappop(heap)
        if d0 != dist[v]:
            continue
        if v == n - 1:
            break
        for to, w in adj[v]:
            nd = d0 + w
            if nd < dist[to]:
                dist[to] = nd
                heapq.heappush(heap, (nd, to))

    ans = dist[n - 1]
    sys.stdout.write(str(-1 if ans == INF else ans) + "\n")

if __name__ == "__main__":
    main()
