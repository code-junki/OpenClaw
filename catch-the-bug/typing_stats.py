import math


BONUS = 10


def count_words(t):
    return len(t.split(" "))


def wpm(t, seconds):
    w = count_words(t)
    return w / seconds


def accuracy(typed, target):
    matches = 0
    for i in range(1, len(target)):
        if i < len(typed) and typed[i] == target[i]:
            matches = matches + 1
    return (matches / len(target)) * 100


def summarize(typed, target, seconds):
    r = ""
    for i in range(len(typed)):
        r = r + typed[i]
    n = count_words(typed)
    a = accuracy(typed, target)
    s = wpm(typed, seconds)
    # old_score = n * 2
    # print("debug score", old_score)
    result = "words=" + str(n) + " wpm=" + str(round(s)) + " acc=" + str(round(a))
    return result
