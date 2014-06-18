#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import numpy as np

class CombinedData(object):
  """
     featuresData -- FeaturesData object (everything about movies)
     usersData -- UsersData object
     weights -- array of 4 doubles: movies weight, user-shared-count weight, user-jaccard weight, user-votes-similarity weight
  """
  
  """Constructor"""
  def __init__(self, featuresData, usersData):
    self.featuresData = featuresData
    self.usersData = usersData
    self.weights = np.array([0.65,  0.005,  0.005,  0.34], dtype=np.float64)
  
  """"""
  def similarity(self, objA, objB):
    userPisiIdA, movieIdA = objA
    userPisiIdB, movieIdB = objB
    moviesSimilarity = self.featuresData.similarity(movieIdA, movieIdB)
    usersSimilarity = self.usersData.similarity(userPisiIdA, userPisiIdB)
    return self.weights[0] * moviesSimilarity + np.dot(self.weights[1:], usersSimilarity)
  
