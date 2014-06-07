#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import numpy as np

class CombinedData(object):
  
  """Constructor"""
  def __init__(self, featuresData, usersData):
    self.featuresData = featuresData
    self.usersData = usersData
    self.weights = np.array([0.0, 1.0/3.0, 1.0/3.0, 1.0/3.0], dtype=np.float64)
  
  """"""
  def similarity(self, objA, objB):
    userPisiIdA, movieIdA = objA
    userPisiIdB, movieIdB = objB
    moviesSimilarity = self.featuresData.similarity(movieIdA, movieIdB)
    usersSimilarity = self.usersData.similarity(userPisiIdA, userPisiIdB)
    return self.weights[0] * moviesSimilarity + np.dot(self.weights[1:], usersSimilarity)
  
