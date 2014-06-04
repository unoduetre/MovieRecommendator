#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import numpy as np
import importlib.machinery

class FeaturesData(object):
  
  """Constructor"""
  def __init__(self, featuresFn='./resources/features/feature.csv', dataFn='./resources/features/data.csv', weightsFn='./resources/features/weight.csv'):
    self.readFeatures(featuresFn)
    self.readRawData(dataFn)
    self.loadFeaturePlugins()
    self.performFeatureExtraction()
    self.loadFeatureWeights(weightsFn)
    self.prepareSubsimilaritiesMatrix()
    self.mask = np.empty(self.featuresCount, dtype=np.bool)
    self.mask.fill(True)
    self.prepareSimilaritiesMatrix()
  
  
  """Read feature names"""
  def readFeatures(self, featuresFn):
    self.featureIdsByName = {}
    for l in filter(None, map(lambda l: l.strip(), open(featuresFn, 'rt').readlines())):
      w = l.split(';')
      featureId = int(w[0])-1 # for 0-indexing
      featureName = w[1]
      self.featureIdsByName[featureName] = featureId
    assert tuple(sorted(self.featureIdsByName.values())) == tuple(range(len(self.featureIdsByName)))
    self.featuresCount = len(self.featureIdsByName)
    
    self.featureNamesById = [None for _ in range(self.featuresCount)]
    for featureName, featureId in self.featureIdsByName.items():
      self.featureNamesById[featureId] = featureName
  
    
  """Read raw samples"""
  def readRawData(self, dataFn):
    self.data = []
    for l in filter(None, map(lambda l: l.strip(), open(dataFn, 'rt').readlines())):
      w = l.split(';')
      movieId = int(w[1])-1 # for 0-indexing
      featureId = int(w[2])-1 # for 0-indexing
      featureValue = w[3]
      if movieId >= len(self.data): self.data.append([None for _ in range(self.featuresCount)])
      self.data[movieId][featureId] = featureValue
    assert sum(row.count(None) for row in self.data) == 0
    
    self.samplesCount = len(self.data)
  
