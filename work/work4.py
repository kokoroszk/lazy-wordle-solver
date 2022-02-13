from util import words

vowels = set(list("aiueoy"))

w = [w for w in words if [c in vowels for c in w].count(True) == 1]
print(len(w))

d = dict()
for _w in w:
    k = _w[:1]
    e = d.get(k) or []
    e.append(_w)
    d[k] = e

for (key, val) in d.items():
    print("%s: %d", (key, len(val)))

values = list(d.values())
result = []


def solve(values, buf):
    if len(set(sum([list(s) for s in buf], []))) % 5 != 0:
        return
    if len(buf) >= 5:
        result.append(buf)
    for i in range(len(values)):
        _values = [*values]
        words = _values.pop(i)
        for word in words:
            solve(_values, buf + [word])


solve(values, [])
