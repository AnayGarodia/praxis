#!/usr/bin/env python3
"""graph6 parser (independent implementation, exact)."""


def parse_g6_line(line):
    line = line.strip()
    if not line:
        return None
    data = [ord(c) - 63 for c in line]
    assert all(0 <= x < 64 for x in data), "bad g6 char"
    if data[0] == 63:
        n = (data[1] << 12) | (data[2] << 6) | data[3]
        bits = data[4:]
    else:
        n = data[0]
        bits = data[1:]
    bitstr = []
    for x in bits:
        for k in range(5, -1, -1):
            bitstr.append((x >> k) & 1)
    E = []
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bitstr[idx]:
                E.append((i, j))
            idx += 1
    return n, E


def load(path):
    out = []
    for line in open(path):
        r = parse_g6_line(line)
        if r:
            out.append(r)
    return out


if __name__ == "__main__":
    import sys
    for n, E in load(sys.argv[1]):
        print(n, len(E))
