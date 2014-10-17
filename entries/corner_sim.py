# Corner Catcher

from math import atan, degrees, pi, factorial, cos, radians
import csv
import re
import sys

keys = {}
key_size = 1.5
for line in open("keypos.csv"):
    k, x, y = map(str.strip, line.split(","))
    keys[k] = float(x), float(y)


def deduplicate(s):
    return s[0] + "".join(s[i + 1] for i in range(len(s) - 1) if s[i + 1] != s[i])


def angle(coord1, coord2):
    x1, y1, x2, y2 = coord1 + coord2
    dx, dy = x2 - x1, y1 - y2
    t = abs(atan(dx/dy)) if dy else pi / 2
    if dx >= 0 and dy >= 0: a = t
    elif dx >= 0 and dy < 0: a = pi - t
    elif dx < 0 and dy >= 0: a = 2 * pi - t
    else: a = t + pi
    return degrees(a)


def significant_letter(swipe):
    if len(swipe) <= 2: return 0
    x1, y1, x2, y2 = keys[swipe[0]] + keys[swipe[-1]]
    m = 0 if x2 == x1 else (y2 - y1) / (x2 - x1)
    y = lambda x: m * (x - x1) + y1
    def sim_fun(x2, y2):
        try: return (x2 / m + y2 - y1 + x1 * m) / (m + 1 / m)
        except ZeroDivisionError: return x2
    dists = []
    for i, key in enumerate(swipe[1:-1]):
        sx, bx = min(x1, x2), max(x1, x2)
        pos_x = max(min(sim_fun(*keys[key]), bx), sx)
        sy, by = min(y1, y2), max(y1, y2)
        pos_y = max(min(y(pos_x), by), sy)
        keyx, keyy = keys[key]
        dist = ((keyx - pos_x) ** 2 + (keyy - pos_y) ** 2) ** 0.5
        a = angle((keyx, keyy), (pos_x, pos_y))
        if 90 <= a <= 180: a = 180 - a
        elif 180 <= a <= 270: a = a - 180
        elif 270 <= a <= 360: a = 360 - a
        if a > 45: a = 90 - a
        h = key_size / 2 / cos(radians(a))
        dists.append((max(dist - h, 0), i + 1, key))
    return sorted(dists, reverse=True)[0][0]


def closeness2(s, t):
    # https://en.wikipedia.org/wiki/Levenshtein_distance
    if s == t: return 0
    if not len(s): return len(t)
    if not len(t): return len(s)
    v0 = list(range(len(t) + 1))
    v1 = list(range(len(t) + 1))
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]
    return v1[len(t)] / len(t)


def possible(swipe, w, s=False):
    m = re.match("^" + "(.*)".join("({})".format(i) for i in w) + "$", swipe)
    if not m or s:
        return bool(m)
    return closeness1(swipe, w) < 0.8


def closeness1(swipe, w):
    m = re.match("^" + "(.*)".join("({})".format(i) for i in w) + "$", swipe)
    unsigpatches = []
    groups = m.groups()
    for i in range(1, len(groups), 2):
        unsigpatches.append(groups[i - 1] + groups[i] + groups[i + 1])
    if debug: print(unsigpatches)
    sig = max(map(significant_letter, unsigpatches))
    if debug: print(sig)
    return sig


def find_closest(swipes):
    level1, level2, level3, level4 = swipes
    if debug: print("Loading words...")
    words = {deduplicate(i.lower()): i.lower() for i in open("wordlist").read().split("\n") if i[0] == level1[0] and i[-1] == level1[-1]}
    if debug: print("Done first filter (start and end):", words)
    r = re.compile("^" + ".*".join(level4) + "$")
    pos_words2 = list(filter(lambda x: bool(r.match(x)), words))
    if debug: print("Done second filter (sharpest points):", pos_words2)
    pos_words = pos_words2 or words
    pos_words = list(filter(lambda x: possible(level1, x), pos_words)) or list(filter(lambda x: possible(level1, x, s=True), pos_words))
    if debug: print("Done third filter (word regex):", pos_words)
    sorted_pos_words = sorted((closeness1(level1, x), -len(x), closeness2(level1, x), x)
                              for x in pos_words)
    if debug: print("Closeness matching (to", level2 + "):", sorted_pos_words)
    return words[sorted_pos_words[0][3]]


def get_corners(swipe):
    corners = [[swipe[0]] for i in range(4)]
    last_dir = last_char = None
    for i in range(len(swipe) - 1):
        dir = angle(keys[swipe[i]], keys[swipe[i + 1]])
        if last_dir is not None:
            d = abs(last_dir - dir)
            a_diff = min(360 - d, d)
            corners[0].append(last_char)
            if debug: print(swipe[i], dir, last_dir, a_diff, end=" ")
            if a_diff >= 55:
                if debug: print("C", end=" ")
                corners[1].append(last_char)
            if a_diff >= 65:
                if debug: print("M", end=" ")
                corners[2].append(last_char)
            if a_diff >= 80:
                if debug: print("S", end=" ")
                corners[3].append(last_char)
            if debug: print()
        last_dir, last_char = dir, swipe[i + 1]
    tostr = lambda x: deduplicate("".join(x + [swipe[-1]]).lower())
    return list(map(tostr, corners))


if __name__ == "__main__":
    debug = "-d" in sys.argv
    if debug: sys.argv.remove("-d")
    swipe = deduplicate(sys.argv[1] if len(sys.argv) > 1 else input()).lower()
    corners = get_corners(swipe)
    if debug: print(corners)
    print(find_closest(corners))
