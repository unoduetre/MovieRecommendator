#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import numpy as np
import random
from ArrayBasedBoundedPriorityQueue import ArrayBasedBoundedPriorityQueue


class VoteGuesser(object):
  
  """Constructor"""
  def __init__(self, combinedData, k=3, trainFn='./resources/dataset/train.csv', taskFn='./resources/dataset/task.csv'):
    self.combinedData = combinedData
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
    pq = ArrayBasedBoundedPriorityQueue(k=self.k)
    for comparedUserId in self.userData:
      if pq.getArray():
        minimalUsefulSimilarity = -pq.getArray()[-1][0]
        comparedUserSimilarityLimit = self.combinedData.similarity((userId, movieId), (comparedUserId, movieId))
        if comparedUserSimilarityLimit < minimalUsefulSimilarity: continue
      for comparedMovieId, vote in self.userData[comparedUserId].items():
        pq.push((-self.combinedData.similarity((userId, movieId), (comparedUserId, comparedMovieId)), vote))
    votes = [vote for _, vote in pq.getArray()]
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
  
  """Calculate some self-validation statistics"""
  def calculateReguessHistogram(self):
    errHistogram = [0 for _ in range(6)]
    for userId in self.userData:
      for movieId in self.userData[userId]:
        realVote = self.userData[userId][movieId]
        del self.userData[userId][movieId]
        guessedVote = self.makeVote(userId, movieId)
        self.userData[userId][movieId] = realVote
        err = abs(guessedVote - realVote)
        print(err, userId, movieId)
        errHistogram[err] += 1
    return errHistogram
  
  """This number is a good measure of how good the method is (the lower the better)"""
  def calculateReguessExpectedError(self):
    errHistogram = self.calculateReguessHistogram()
    return sum(errHistogram[i] * i for i in range(6)) / sum(errHistogram)
  
  """Print some self-validation statistics"""
  def printReguessReport(self):
    errHistogram = self.calculateReguessHistogram()
    totalCount = sum(errHistogram)
    # difference between guessedVote and realVote: how often did it occur
    for i in range(6):
      print('%d:' % i, '%.2f%%' % (100.0 * errHistogram[i] / totalCount))
    print(sum(errHistogram[i] * i for i in range(6)) / sum(errHistogram))
  
