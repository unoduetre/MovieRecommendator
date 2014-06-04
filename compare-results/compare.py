#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os

assert len(sys.argv) >= 3

aFn, bFn = sys.argv[1:3]

assert os.path.exists(aFn)
assert os.path.exists(bFn)

def read(fn):
  votes = {}
  for line in filter(None, map(lambda l: l.strip(), open(fn, 'rt'))):
    words = list(map(lambda w: w.strip(), line.split(';')))
    pisiId = int(words[0])
    vote = int(words[3])
    votes[pisiId] = vote
  return votes

aVotes = read(aFn)
bVotes = read(bFn)

assert aVotes.keys() == bVotes.keys()

count = len(aVotes)
similar = 0
quiteSimilar = 0
errSum = 0

for pisiId in aVotes:
  err = abs(aVotes[pisiId] - bVotes[pisiId])
  errSum += err
  similar += (err == 0)
  quiteSimilar += (err <= 1)

avgErr = errSum / count

print('Similar votes: %.2f%%' % (similar * 100.0 / count))
print('1-star precision: %.2f%%' % (quiteSimilar * 100.0 / count))
print('Average error: %f' % avgErr)
