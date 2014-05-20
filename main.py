#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from FeaturesData import *
from ArrayBasedBoundedPriorityQueue import ArrayBasedBoundedPriorityQueue

def makeVote(fd, reqMovieId, data):
  pq = ArrayBasedBoundedPriorityQueue(k=3)
  for movieId, vote in data.items():
    pq.push((-fd.similarity(reqMovieId, movieId), movieId))
  notes = [data[movieId] for _, movieId in pq.getArray()]
  return int(0.5 + sum(notes) / len(notes))


def main():
  os.chdir(os.path.dirname(sys.argv[0]))
  fd = FeaturesData()
  
  trainFn = './resources/dataset/train.csv'
  taskFn = './resources/dataset/task.csv'
  
  userData = {}
  
  for l in filter(None, map(lambda l: l.strip(), open(trainFn, 'rt').readlines())):
    w = l.split(';')
    userId = int(w[1])
    movieId = int(w[2])-1 # for 0-indexing
    vote = int(w[3])
    if userId not in userData: userData[userId] = {}
    userData[userId][movieId] = vote
  
  outputFn = './output/task.csv'
  
  outputFh = open(outputFn, 'wt')
  for l in filter(None, map(lambda l: l.strip(), open(taskFn, 'rt').readlines())):
    w = l.split(';')
    pisiId = int(w[0])
    userId = int(w[1])
    movieId = int(w[2])-1 # for 0-indexing
    vote = makeVote(fd, movieId, userData[userId])
    outputFh.write('%d;%d;%d;%d\n' % (pisiId, userId, movieId+1, vote))
  outputFh.close()


if __name__ == '__main__':
  main()
