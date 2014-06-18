#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import numpy as np

class CFSolver(object):
  
  """"""
  def __init__(self, featuresCount, trainFn='./resources/dataset/train.csv'):
    self.featuresCount = featuresCount
    self.trainFn = trainFn
    self.readData()
    self.prepareVotesMatrix()
    self.initializeFeatures()
  
  """"""
  def readData(self):
    self.userDataByPisiId = {}
    maxMovieId = 0
    for l in filter(None, map(lambda l: l.strip(), open(self.trainFn, 'rt').readlines())):
      w = l.split(';')
      userPisiId = int(w[1])
      movieId = int(w[2])-1 # for 0-indexing
      maxMovieId = max(maxMovieId, movieId)
      vote = int(w[3])
      if userPisiId not in self.userDataByPisiId: self.userDataByPisiId[userPisiId] = {}
      self.userDataByPisiId[userPisiId][movieId] = vote
    self.userPisiIds = sorted(self.userDataByPisiId.keys())
    self.userIdsByPisiId = {}
    for userId, userPisiId in enumerate(self.userPisiIds): self.userIdsByPisiId[userPisiId] = userId
    self.userData = [self.userDataByPisiId[userPisiId] for userPisiId in self.userPisiIds]
    self.usersCount = len(self.userPisiIds)
    self.moviesCount = maxMovieId + 1
    
  """"""
  def prepareVotesMatrix(self):
    self.normalizedVotesMatrix = np.empty([self.usersCount, self.moviesCount], dtype=np.float64)
    self.normalizedVotesMatrix.fill(-1.0)
    for userId in range(self.usersCount):
      for movieId, vote in self.userData[userId].items():
        self.normalizedVotesMatrix[userId, movieId] = vote * 0.2
    self.knownVotesMask = (self.normalizedVotesMatrix != -1.0)
    self.knownVotesCount = np.sum(self.knownVotesMask)
  
  """"""
  def initializeFeatures(self):
    self.weights = np.random.rand(self.usersCount, self.featuresCount) * 0.875 + 0.0625
    self.features = np.random.rand(self.moviesCount, self.featuresCount) * 0.875 + 0.0625
    print(self.meanSquareError())
    print(self.meanSquareError2())
  
  """"""
  def calculateNormalizedVoteAt(self, userId, movieId):
    return np.dot(self.weights[userId], self.features[movieId])
  
  """"""
  def calculateErrorAt(self, userId, movieId):
    # assert self.normalizedVotesMatrix[userId, movieId] != -1
    return self.normalizedVotesMatrix[userId, movieId] - self.calculateNormalizedVoteAt(userId, movieId)
  
  """This square error is totally mean and unkind towards us."""
  def meanSquareError(self):
    count = 0
    sqSum = 0.0
    for userId in range(self.usersCount):
      for movieId in range(self.moviesCount):
        if self.normalizedVotesMatrix[userId, movieId] != -1.0:
          count += 1
          sqSum += self.calculateErrorAt(userId, movieId) ** 2
    return sqSum / count
  
  """This square error is totally mean and unkind towards us."""
  def meanSquareError2(self):
    self.calculatedMatrix = np.dot(self.weights, self.features.transpose())
    return np.sum(((self.calculatedMatrix - self.normalizedVotesMatrix) ** 2) * self.knownVotesMask) / self.knownVotesCount



