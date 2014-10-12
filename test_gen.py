import random
import sys

if len(sys.argv) > 1 and "add":
    mode = "a"
else:
    mode = "w"

words = open("wordlist").read().split("\n")
with open("testlist", mode) as tests:
    for i in range(150):
        word = random.choice(words)
        words.remove(word)
        swipe = input(word + ": ")
        while swipe[0] != word[0] or swipe[-1] != word[-1]:
            swipe = input(word + ": ")
        tests.write(word + " " + swipe + "\n")
