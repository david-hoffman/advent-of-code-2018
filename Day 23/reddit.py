import re


re_digits = re.compile(r"-?\d+")


def strip_digits(input_):
    """Strip numbers from a string"""
    return list(map(int, re_digits.findall(input_)))


def get_bots(values):
    bots = [strip_digits(line) for line in values.splitlines()]
    return bots


def calc(values):
    bots = get_bots(values)
    best_i = None
    best_val = None
    for i in range(len(bots)):
        if best_i is None or bots[i][3] > best_val:
            best_val = bots[i][3]
            best_i = i

    bx, by, bz, bdist = bots[best_i]

    ret = 0

    for i in range(len(bots)):
        x, y, z, _dist = bots[i]

        if abs(x - bx) + abs(y - by) + abs(z - bz) <= bdist:
            ret += 1

    return ret


def calc2(values):
    bots = get_bots(values)
    print(bots)
    xs = [x[0] for x in bots]
    ys = [x[1] for x in bots]
    zs = [x[2] for x in bots]

    dist = 1
    while dist < max(xs) - min(xs):
        dist *= 2

    while True:
        target_count = 0
        best = None
        best_val = None
        for x in range(min(xs), max(xs) + 1, dist):
            for y in range(min(ys), max(ys) + 1, dist):
                for z in range(min(zs), max(zs) + 1, dist):
                    count = 0
                    for bx, by, bz, bdist in bots:
                        calc = abs(x - bx) + abs(y - by) + abs(z - bz)
                        if (calc - bdist) / dist <= 1:
                            count += 1
                    if count > target_count:
                        target_count = count
                        best_val = abs(x) + abs(y) + abs(z)
                        best = (x, y, z)
                    elif count == target_count and best_val:
                        if abs(x) + abs(y) + abs(z) < best_val:
                            best_val = abs(x) + abs(y) + abs(z)
                            best = (x, y, z)

        if dist == 1:
            return best_val, target_count
        else:
            xs = [best[0] - dist, best[0] + dist]
            ys = [best[1] - dist, best[1] + dist]
            zs = [best[2] - dist, best[2] + dist]
            dist = (dist + 1) // 2


def run(values):
    print("Nearest the big bot: " + str(calc(values)))
    print("Best location value: " + str(calc2(values)))


if __name__ == '__main__':

    with open("input.txt", "r") as fp:
        run(fp.read())