from random import random


def load():
    with open("./src.txt") as f:
        d = f.readline()
        return set(d.split(","))


words = load()

vowels = ["a", "i", "u", "e", "o"]

letters_ord_high_frequency = "JQXZWVFYBHKMPGUDCLOTNRAISE"
letters_ord_low_freqency = "".join(list(reversed(letters_ord_high_frequency)))


def frequency(c):
    return letters_ord_high_frequency.index(c.upper())


word = list(words)[int(random()*10000)]
# print("word: %s" % word)


def wordle(ans):
    result = [""] * 5
    match = []
    for i in range(len(ans)):
        if ans[i] == word[i]:
            result[i] = "g"
            match.append(ans[i])

    for i in range(len(ans)):
        if result[i] != "g" and ans[i] in word and match.count(ans[i]) < word.count(ans[i]):
            result[i] = "y"
            match.append(ans[i])

    return result
