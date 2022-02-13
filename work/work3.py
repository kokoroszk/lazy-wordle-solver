# memo
# 実際にwordleを解いてみた
# 解くことはできたが、試行回数が6回を超えるのでチューニングが必要か...

from util import frequency, wordle
from work2 import generateAnswers

# init answers
vowel_and_high_frequency_letters = [
    "aurei",
    "stoln",
    "gyppy"
]
low_frequency_letters = [
    "jumby",
    "vozhd",
    "waqfs",
    "pixel"
]
# high_frequency_letters = [
#     "raise", "count", "glyph", "miked",  # i, e
# ]

mixed = [
    "aurei",
    "jumby",
    "vozhd",
]
# high_frequency_low_vowles = ["rynds", "cloth", "muzak", "bewig"]
# high_frequency_low_vowles = ["rynds", "clept", "gumbo", "khazi"]
high_frequency_low_vowles = ["rynds", "mulct", "bigha", "kopje"]
high_frequency_without_e = ["crwth", "kynds", "jumbo", "pilaf"]
init_answers = high_frequency_low_vowles


fixed = ["", "", "", "", ""]
included = []
excluded = set()
checked = set()


def checkResult(ans, ret):
    if ["g", "g", "g", "g", "g"] == ret:
        return True

    wbuf = dict()
    for w in ans:
        n = wbuf.get(w) or 0
        wbuf[w] = n + 1

    for i in range(len(ret)):
        if ret[i] == "g":
            fixed[i] = ans[i]
            if ans[i] in included:
                included.remove(ans[i])

    ybuf = dict()
    for i in range(len(ret)):
        if ret[i] == "y":
            buf = ybuf.get(ans[i]) or 0
            ybuf[ans[i]] = buf + 1
    for (k, v) in ybuf.items():
        num = included.count(k)
        for _ in range(num, v):
            included.append(k)
        if wbuf[k] > v:
            # XXX 候補作成の処理順序のおかげで、excludedに単純に追加して動く
            # ここで英字kがv個含まれることが確定 + includedに英字kをv個が追加されている
            # fixedとincludedから候補を作成 -> 全alphaからexcludedを除外した中で単語を作成する
            # fixed+includedに追加する英字候補としては、excludeでよい
            excluded.add(k)

    for i in range(len(ret)):
        if ret[i] == "":
            if not ans[i] in included:
                excluded.add(ans[i])
    return False


def d1(s): return " " if s == "" else s
def debug(l): return [d1(x) for x in l]


def refineExclude(fixed, included, excluded, checked):
    a = alphas.copy()
    for d in generateAnswers(fixed, included, excluded, checked):
        for c in d:
            a.discard(c)
    return excluded.union(a)


correct = False
trycnt = 0
for ans in init_answers:
    trycnt += 1
    checkResult(ans, wordle(ans))
    if correct:
        break

alphas = set(list("abcdefghijklmnopqrstuvwxyz"))


while (not correct):
    ans = ""
    maxFreqScore = -1
    for d in generateAnswers(fixed, included, excluded, checked):
        trycnt += 1
        freqScore = sum([frequency(c) for c in d])
        if freqScore > maxFreqScore:
            maxFreqScore = freqScore
            ans = d
    assert(ans != "")
    ret = wordle(ans)
    correct = checkResult(ans, wordle(ans))
    checked.add("".join(ans))

print("%s\t%d" % ("".join(ans), trycnt))
