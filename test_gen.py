import random

words = open("wordlist").read().split("\n")
with open("testlist", "w") as tests:
    for i in range(50):
        word = random.choice(words)
        words.remove(word)
        swipe = input(word + ": ")
        tests.write(word + " " + swipe + "\n")