#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from ArrayBasedBoundedPriorityQueue import ArrayBasedBoundedPriorityQueue


class VoteGuesser(object):
  
  """Constructor"""
  def __init__(self, featuresData, k=3, trainFn='./resources/dataset/train.csv', taskFn='./resources/dataset/task.csv'):
    self.featuresData = featuresData
    self.k = k
    self.trainFn = trainFn
    self.taskFn = taskFn
    self.userData = {}
    self.readUserData()
  
  """Reading training data"""
  def readUserData(self):
    for l in filter(None, map(lambda l: l.strip(), open(self.trainFn, 'rt').readlines())):
      w = l.split(';')
      userId = int(w[1])
      movieId = int(w[2])-1 # for 0-indexing
      vote = int(w[3])
      if userId not in self.userData: self.userData[userId] = {}
      self.userData[userId][movieId] = vote
  
  """Guessing a single vote"""
  def makeVote(self, userId, movieId):
    thisUserData = self.userData[userId]
    pq = ArrayBasedBoundedPriorityQueue(k=self.k)
    for otherMovieId, vote in thisUserData.items():
      pq.push((-self.featuresData.similarity(movieId, otherMovieId), otherMovieId))
    votes = [thisUserData[otherMovieId] for _, otherMovieId in pq.getArray()]
    return int(round(sum(votes) / len(votes)))
  
  """Guessing all the votes from the task"""
  def solveTask(self, outputFn='./output/task.csv'):
    outputFh = open(outputFn, 'wt')
    for l in filter(None, map(lambda l: l.strip(), open(self.taskFn, 'rt').readlines())):
      w = l.split(';')
      pisiId = int(w[0])
      userId = int(w[1])
      movieId = int(w[2])-1 # for 0-indexing
      vote = self.makeVote(userId, movieId)
      outputFh.write('%d;%d;%d;%d\n' % (pisiId, userId, movieId+1, vote))
    outputFh.close()
  
  """Print some self-validation statistics"""
  def printReguessReport(self):
    errHistogram = [0 for _ in range(6)]
    for userId in self.userData:
      for movieId in self.userData[userId]:
        realVote = self.userData[userId][movieId]
        del self.userData[userId][movieId]
        guessedVote = self.makeVote(userId, movieId)
        self.userData[userId][movieId] = realVote
        err = abs(guessedVote - realVote)
        errHistogram[err] += 1
    totalCount = sum(errHistogram)
    # difference between guessedVote and realVote: how often did it occur
    for i in range(6):
      print('%d:' % i, '%.2f%%' % (100.0 * errHistogram[i] / totalCount))
    print(sum(errHistogram[i] * i for i in range(6)) / sum(errHistogram))
  
  """Print some self-validation statistics"""
  def printSimilarityReport(self):
    similaritiesByVoteDiff = [[] for _ in range(6)]
    for userId in self.userData:
      for movieIdA in self.userData[userId]:
        for movieIdB in self.userData[userId]:
          if movieIdA == movieIdB: continue
          diff = abs(self.userData[userId][movieIdA] - self.userData[userId][movieIdB])
          similaritiesByVoteDiff[diff].append(self.featuresData.similarity(movieIdA, movieIdB))
    # difference between votes for a pair of movies: average similarity between them
    for i in range(6):
      print('%d:' % i, '%f' % (sum(similaritiesByVoteDiff[i]) / len(similaritiesByVoteDiff[i])))



