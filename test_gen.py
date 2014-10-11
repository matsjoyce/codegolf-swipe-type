import random

words = open("wordlist").read().split("\n")
with open("testlist", "w") as tests:
    for i in range(100):
        word = random.choice(words)
        words.remove(word)
        swipe = input(word + ": ")
        while swipe[0] != word[0] or swipe[-1] != word[-1]:
            swipe = input(word + ": ")
        tests.write(word + " " + swipe + "\n")
