#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import numpy as np

class UsersData(object):
  
  """Constructor"""
  def __init__(self, trainFn='./resources/dataset/train.csv'):
    self.trainFn = trainFn
    self.userDataByPisiId = {}
    self.readUserData()
    self.prepareSharedCountsMatrix()
    self.prepareWatchedJaccardMatrix()
    self.prepareVotesSimilarityMatrix()
  
  """Reading training data"""
  def readUserData(self):
    for l in filter(None, map(lambda l: l.strip(), open(self.trainFn, 'rt').readlines())):
      w = l.split(';')
      userPisiId = int(w[1])
      movieId = int(w[2])-1 # for 0-indexing
      vote = int(w[3])
      if userPisiId not in self.userDataByPisiId: self.userDataByPisiId[userPisiId] = {}
      self.userDataByPisiId[userPisiId][movieId] = vote
    self.userPisiIds = sorted(self.userDataByPisiId.keys())
    self.userIdsByPisiId = {}
    for userId, userPisiId in enumerate(self.userPisiIds): self.userIdsByPisiId[userPisiId] = userId
    self.userData = [self.userDataByPisiId[userPisiId] for userPisiId in self.userPisiIds]
    self.usersCount = len(self.userPisiIds)
  
  
  """"""
  def calculateSubsimilarity(self, k, l, userFatureId):
    if userFeatureId == 1: return self.count
  
  
  """Precalculate shared movies counts matrix"""
  def prepareSharedCountsMatrix(self):
    self.sharedCountsMatrix = np.empty([self.usersCount, self.usersCount], dtype=np.float64)
    for k in range(self.usersCount):
      for l in range(k+1):
        self.sharedCountsMatrix[k, l] = len(self.userData[k].keys() & self.userData[l].keys())
        self.sharedCountsMatrix[l, k] = self.sharedCountsMatrix[k, l]
    self.sharedCountsMatrix /= np.max(self.sharedCountsMatrix)
    for k in range(self.usersCount): self.sharedCountsMatrix[k, k] = 1.0
  
  """Precalculate watched movies sets Jaccard coefficients matrix"""
  def prepareWatchedJaccardMatrix(self):
    self.watchedJaccardMatrix = np.empty([self.usersCount, self.usersCount], dtype=np.float64)
    for k in range(self.usersCount):
      for l in range(k+1):
        self.watchedJaccardMatrix[k, l] = len(self.userData[k].keys() & self.userData[l].keys()) / len(self.userData[k].keys() | self.userData[l].keys())
        self.watchedJaccardMatrix[l, k] = self.watchedJaccardMatrix[k, l]
  
  """"""
  def calculateVotesSimilarity(self, k, l):
    movieIds = self.userData[k].keys() & self.userData[l].keys()
    if len(movieIds) == 0: return 0.0
    errSum = 0.0
    for movieId in movieIds:
      voteK = self.userData[k][movieId]
      voteL = self.userData[l][movieId]
      errSum += abs(voteK - voteL)
    return 1.0 - (errSum / (len(movieIds) * 5.0))
  
  """Precalculate votes similarity matrix"""
  def prepareVotesSimilarityMatrix(self):
    self.votesSimilarityMatrix = np.empty([self.usersCount, self.usersCount], dtype=np.float64)
    for k in range(self.usersCount):
      for l in range(k+1):
        self.votesSimilarityMatrix[k, l] = self.calculateVotesSimilarity(k, l)
        self.votesSimilarityMatrix[l, k] = self.votesSimilarityMatrix[k, l]
  
  def similarity(self, kPisiId, lPisiId):
    k = self.userIdsByPisiId[kPisiId]
    l = self.userIdsByPisiId[lPisiId]
    return np.array([
        self.sharedCountsMatrix[k, l],
        self.watchedJaccardMatrix[k, l],
        self.votesSimilarityMatrix[k, l]
      ], dtype=np.float64)
  
