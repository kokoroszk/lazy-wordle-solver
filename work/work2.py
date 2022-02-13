# memo
# 候補生成ロジックを考えてみた
# また、それを利用して、序盤の定石wordを考えてみている

from util import frequency, letters_ord_high_frequency, load, words


def comb(all, buf, result, fixed):
    if len(buf) == 5:
        result.append(",".join(buf))
        return

    if fixed[len(buf)] != "":
        comb(all, buf + [fixed[len(buf)]], result, fixed)
        return

    for d in all:
        comb(all, buf + [d], result, fixed)


def uniq_comb(all, buf, result, fixed):
    if len(buf) == 5:
        result.append(",".join(buf))
        return
    if fixed[len(buf)] != "":
        uniq_comb(all, buf + [fixed[len(buf)]], result, fixed)
        return
    for d in all:
        _all = [*all]
        _all.remove(d)
        uniq_comb(_all, buf + [d], result, fixed)


def generateWords(letters, fixed, excluded):
    lttrs = list(filter(lambda x: not x in excluded, letters))
    result = []
    comb(lttrs, [], result, fixed)
    result = [s.split(",") for s in set(result)]
    return list(filter(lambda x: "".join(x) in words, result))


def uniq_generateWords(letters, fixed, excluded):
    lttrs = list(filter(lambda x: not x in excluded, letters))
    result = []
    uniq_comb(lttrs, [], result, fixed)
    result = [s.split(",") for s in set(result)]
    return list(filter(lambda x: "".join(x) in words, result))


def makeCandidate(fixed, included):
    f = []
    letters = [*included]
    fixedCnt = sum(i != "" for i in fixed)
    for i in range(len(included)+fixedCnt, 5):
        letters.append("")

    # XXX setにするので、順序は安定しない..
    result = []
    uniq_comb(letters, [], result, fixed)
    result = [s.split(",") for s in set(result)]
    return result


fixed = ["", "", "", "e", "r"]

# print(generateWords(letters_ord_high_frequency.lower(), fixed, []))


def generateAnswers(fixed, included, excluded, checked):
    # print("conditions:: fixed: %s, included: %s, excluded: %s" %
    #       (str(fixed), str(included), str(excluded)))
    result = []
    for cand in makeCandidate(fixed, included):
        result.extend(generateWords(
            letters_ord_high_frequency.lower(), cand, excluded))
    return [r for r in result if not "".join(r) in checked]


def uniq_generateAnswers(fixed, included, excluded, checked):
    # print("conditions:: fixed: %s, included: %s, excluded: %s" %
    #       (str(fixed), str(included), str(excluded)))
    result = []
    for cand in makeCandidate(fixed, included):
        result.extend(uniq_generateWords(
            letters_ord_high_frequency.lower(), cand, excluded))
    return [r for r in result if not "".join(r) in checked]


# for a in generateAnswers(["o", "", "d", "e", "r"], [], ["l"]):
#     print(*a)

def f(l): return sum([list(s) for s in l], [])


def make(test):
    return uniq_generateAnswers(["", "", "", "", ""], [], test, set())


def choise(answers):
    ans = ""
    maxFreqScore = -1
    minFreqScore = 9999999999999
    for d in answers:
        freqScore = sum([frequency(c) for c in d])
        if freqScore > maxFreqScore:
            # if freqScore < minFreqScore:
            maxFreqScore = freqScore
            minFreqScore = freqScore
            ans = d
    return ans


# test = set(f(["crwth", "kynds", "jumbo", "pilaf"]))
# answers = []
# print("\n".join(["".join(s) for s in make(test)]))
# print(choise(make(test)))

# for word in make(test):
#     s2 = test.copy().union(word)
#     for w2 in make(s2):
#         s3 = s2.union(w2)
#         # answers.append(s3)
#         for w4 in make(s3):
#             answers.append(s3.union(w4))
#             print(s3.union(w4))

# print(answers)

# answers = set()
# for i in range(len("raisecountglyph")-1):
#     for j in range(len("raisecountglyph")):
#         w = list("raisecountglyph")
#         w.pop(i)
#         w.pop(j-1)
#         answers.add("".join(make(set(w))))

# print(choise(answers))
