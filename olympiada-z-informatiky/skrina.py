import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    q = int(next(it))

    MAXV = 10 ** 6

    spf = list(range(MAXV + 1))
    limit = int(MAXV ** 0.5) + 1
    for i in range(2, limit):
        if spf[i] == i:
            for j in range(i * i, MAXV + 1, i):
                if spf[j] == j:
                    spf[j] = i

    cnt = [0] * (MAXV + 1)
    skrina = set()
    out = []

    for _ in range(q):
        t = int(next(it))
        x = int(next(it))

        factors = []
        n = x
        while n > 1:
            p = spf[n]
            factors.append(p)
            while n % p == 0:
                n //= p

        if t == 1:
            if any(cnt[p] > 0 for p in factors):
                out.append("nie")
            else:
                for p in factors:
                    cnt[p] += 1
                skrina.add(x)
                out.append("ano")
        else:
            if x in skrina:
                skrina.remove(x)
                for p in factors:
                    cnt[p] -= 1

    if out:
        sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
