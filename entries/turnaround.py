import sys, csv, re

wordlistfile = open('wordlist', 'r')
wordlist = wordlistfile.read().split('\n')

layout = 'qwertyuiop asdfghjkl  zxcvbnm'
keypos = dict((l, (2*(i%11)+i/11, i/11)) for i,l in enumerate(layout))

#read input from command line argument
input = sys.argv[1]

#remove repeated letters
input = ''.join(x for i,x in enumerate(input) if i==0 or x!=input[i-1])

#find positions of letters on keyboard
xpos = map(lambda l: keypos[l][0], input)
ypos = map(lambda l: keypos[l][1], input)

#check where the direction changes (neglect slight changes in x, e.g. 'edx')
xpivot = [(t-p)*(n-t)<-1.1 for p,t,n in zip(xpos[:-2], xpos[1:-1], xpos[2:])]
ypivot = [(t-p)*(n-t)<0 for p,t,n in zip(ypos[:-2], ypos[1:-1], ypos[2:])]
pivot = [xp or yp for xp,yp in zip(xpivot, ypivot)]

#the first and last letters are always pivots
pivot = [True] + pivot + [True]

#build regex
regex = ''.join(x + ('+' if p else '*') for x,p in zip(input, pivot))
regexobj = re.compile(regex + '$')

#find all words that match the regex and output the longest one
words = [w for w in wordlist if regexobj.match(w)]
output = max(words, key=len) if words else input
print output