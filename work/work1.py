# memo
# 初手で母音を特定するとわかりやすいかな...など思い、母音を一番多く含む単語を考えてみた
# 後で思ったが、そんなに効果はなさそう...

from util import frequency, load, vowels


def s(l):
    return "".join(l)


def comb(all, buf, result):
    if len(buf) == 5:
        result.append(buf)
    for d in all:
        if d in buf:
            continue
        comb(all, buf + [d], result)


# almost 13000 < 10 ** 5
words = load()


# 120 < 10 ** 3
vowelPairs = []
comb(vowels, [], vowelPairs)


def leven(w1, w2):
    cnt = 0
    for i in range(len(w1)):
        if w1[i] != w2[i]:
            cnt += 1
    return cnt


# 130000 < 10**8
# m = {}
# for v in vowelPairs:
#     for w in words:
#         lev = leven(v, w)
#         e = m.get(lev) or []
#         e.append(v)
#         m[lev] = e

"""
levenshtein deistance
5 1048741
4 451458
3 52014
2 1418
1 9
"""
# for (k, v) in m.items():
#     print(k, len(v))

# for v in m[1]:
#     print(s(v))


cand = []
for v in vowelPairs:
    for w in words:
        lev = leven(v, w)
        if lev == 1:
            cand.append([v, w])


def notVowel(word):
    for i in range(len(word)):
        if not word[i] in vowels:
            return (i, word[i])


"""
vowels word include freq exclude freq
aueio audio d 15 e 25
aueoi auloi l 17 e 25
auoei aurei r 21 o 18
aoieu adieu d 15 o 18
aouie louie l 17 a 22
uoaei uraei r 21 o 18
eiaou miaou m 11 e 25
ouaie ourie r 21 a 22
ouiea ouija j 0 e 25
"""
max_frequency = -1
result = ""
for d in cand:
    idx, c = notVowel(d[1])
    f = frequency(c)
    print(s(d[0]), d[1], c, f, d[0][idx], frequency(d[0][idx]))
    if (f > max_frequency):
        max_frequency = f
        result = d[1]

# aurei (not includes o)
print(result)
