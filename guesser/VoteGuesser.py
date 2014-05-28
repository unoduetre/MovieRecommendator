#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import numpy as np
import random
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
        errHistogram[err] += 1
    return errHistogram
  
  """This number is a good measure of how good the method is (the lower the better)"""
  def calculateReguessExpectedError(self):
    errHistogram = self.calculateReguessHistogram()
    return sum(errHistogram[i] * i for i in range(6)) / sum(errHistogram)
  
  """Calculate some self-validation statistics"""
  def calculateReguessHistogramFromSample(self, sample):
    errHistogram = [0 for _ in range(6)]
    for userId in sample:
      for movieId in self.userData[userId]:
        realVote = self.userData[userId][movieId]
        del self.userData[userId][movieId]
        guessedVote = self.makeVote(userId, movieId)
        self.userData[userId][movieId] = realVote
        err = abs(guessedVote - realVote)
        errHistogram[err] += 1
    return errHistogram
  
  """This number is a good measure of how good the method is (the lower the better)"""
  def calculateReguessExpectedErrorFromSample(self, sample):
    errHistogram = self.calculateReguessHistogramFromSample(sample)
    return sum(errHistogram[i] * i for i in range(6)) / sum(errHistogram)
  
  """Print some self-validation statistics"""
  def printReguessReport(self):
    errHistogram = self.calculateReguessHistogram()
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
  
  """Pass the weights-resetting call to featureData"""
  def resetWeights(self):
    self.featuresData.resetWeights()
  
  """Single weight adjustment"""
  def adjustWeight(self, featureGroup, r=2.0):
    tmpWeights = np.copy(self.featuresData.weights)
    bestErr, bestWeight = self.calculateReguessExpectedError(), tmpWeights[featureGroup[0]]
    w0 = tmpWeights[featureGroup[0]]
    for i in range(5):
      if i == 2: continue
      e = (i * 0.25 - 0.5) * (2.0 * r)
      w = w0 * 10 ** e
      self.featuresData.weights = np.copy(tmpWeights)
      for featureId in featureGroup: self.featuresData.weights[featureId] = w
      self.featuresData.normalizeWeights()
      self.featuresData.prepareSimilaritiesMatrix()
      err = self.calculateReguessExpectedError()
      if err < bestErr:
        bestErr, bestWeight = err, w
    self.featuresData.weights = np.copy(tmpWeights)
    for featureId in featureGroup: self.featuresData.weights[featureId] = bestWeight
    self.featuresData.normalizeWeights()
    self.featuresData.prepareSimilaritiesMatrix()
    if bestWeight != w0:
      print(featureGroup, w0, '->', self.featuresData.weights[featureGroup[0]], bestErr)
    else:
      print(featureGroup, w0, 'unchanged')
    if r > 0.5:
      self.adjustWeight(featureGroup, r / 3.0)
  
  """Full weigths adjustment"""
  def adjustWeights(self, loops=1):
    for loop in range(loops):
      if loops != 1: print('LOOP', loop+1, '/', loops)
      featureGroups = self.featuresData.getFeatureGroups()
      random.shuffle(featureGroups)
      for featureGroup in featureGroups:
        self.adjustWeight(featureGroup)
  
  
  """"""
  def selectFeatures(self, logFn='./output/selection.txt'):
    tmpMask = np.empty(self.featuresData.featuresCount, dtype=np.bool)
    self.featuresData.mask.fill(False)
    bestErr = float('+inf')
    
    logFile = open(logFn, 'wt')
    
    while True:
      someAdditions = False
      while True:
        changed = False
        options = []
        for featureId in range(self.featuresData.featuresCount):
          if self.featuresData.mask[featureId] == False:
            options.append(featureId)
        random.shuffle(options)
        for featureId in options:
          self.featuresData.mask[featureId] = True
          self.featuresData.prepareSimilaritiesMatrix()
          err = self.calculateReguessExpectedError()
          if err < bestErr:
            print('+', featureId, err)
            logFeatures = ','.join(map(lambda i:str(i+1), filter(lambda featureId: self.featuresData.mask[featureId] == True, list(featureId for featureId in range(self.featuresData.featuresCount)))))
            logFile.write('{%s} -> %s\n' % (logFeatures, err))
            logFile.flush()
            bestErr = err
            changed = True
            someAdditions = True
            break
          self.featuresData.mask[featureId] = False
        if not changed: break
      
      someRemovals = False
      while True:
        changed = False
        options = []
        for featureId in range(self.featuresData.featuresCount):
          if self.featuresData.mask[featureId] == True:
            options.append(featureId)
        random.shuffle(options)
        for featureId in options:
          self.featuresData.mask[featureId] = False
          self.featuresData.prepareSimilaritiesMatrix()
          err = self.calculateReguessExpectedError()
          if err < bestErr:
            print('-', featureId, err)
            logFeatures = ','.join(map(lambda i:str(i+1), filter(lambda featureId: self.featuresData.mask[featureId] == True, list(featureId for featureId in range(self.featuresData.featuresCount)))))
            logFile.write('{%s} -> %s\n' % (logFeatures, err))
            logFile.flush()
            bestErr = err
            changed = True
            someRemovals = True
            break
          self.featuresData.mask[featureId] = True
        if not changed: break
      
      if not (someAdditions or someRemovals): break
    
    logFile.close()
    
    self.featuresData.prepareSimilaritiesMatrix()
  
  
  """Pass the weights-serializing call to featureData"""
  def serializeWeights(self, outWeightsFn='./output/weight.csv'):
    self.featuresData.serializeWeights(outWeightsFn)
   
  
  """Pass the mask-serializing call to featureData"""
  def serializeMask(self, outMaskFn='./output/mask.csv'):
    self.featuresData.serializeMask(outMaskFn)
   
  
  """Pass the mask-loading call to featureData"""
  def loadMask(self, maskFn='./resources/mask.csv'):
    self.featuresData.loadMask(maskFn)

