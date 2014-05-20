#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import numpy as np
import importlib.machinery

class FeaturesData(object):
  
  """Constructor"""
  def __init__(self, featuresFn='./resources/features/feature.csv', dataFn='./resources/features/data.csv', weightsFn='./resources/features/weight.csv'):
    
    """Read feature names"""
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
    
    """Load plugins"""
    self.featureSupportByName = {}
    for pluginFileBasename in os.listdir('plugins'):
      if not pluginFileBasename.endswith('.py'): continue
      pluginFn = os.path.join('plugins', pluginFileBasename)
      name = pluginFileBasename[:-3]
      loader = importlib.machinery.SourceFileLoader(name, pluginFn)
      module = loader.load_module()
      for featureName, featureSupportLoader in module.featureSupportLoadersByName.items():
        assert featureName not in self.featureSupportByName
        featureId = self.featureIdsByName[featureName]
        self.featureSupportByName[featureName] = featureSupportLoader(self, featureId)
    
    for k in self.featureIdsByName: assert k in self.featureSupportByName
    
    self.featureSupportById = [None for _ in range(self.featuresCount)]
    for featureName, featureSupport in self.featureSupportByName.items():
      featureId = self.featureIdsByName[featureName]
      self.featureSupportById[featureId] = featureSupport
    
    """Extract features from raw data"""
    self.extractedData = []
    for i, row in enumerate(self.data):
      self.extractedData.append([None for _ in range(self.featuresCount)])
      for j in range(self.featuresCount):
        self.extractedData[i][j] = self.featureSupportById[j].extract(i)
    
    """Load weights"""
    self.weights = np.empty(self.featuresCount, dtype=np.float64)
    self.weights.fill(-1.0)
    for l in filter(None, map(lambda l: l.strip(), open(weightsFn, 'rt').readlines())):
      w = l.split(';')
      featureName = w[0]
      featureId = self.featureIdsByName[featureName]
      weight = float(w[1])
      self.weights[featureId] = weight
    assert np.min(self.weights) >= 0.0
    assert abs(np.sum(self.weights) - 1.0) < 1e-10
    
    """Precalculate similarities matrix"""
    self.similaritiesMatrix = np.empty([self.samplesCount, self.samplesCount], dtype=np.float64)
    for k in range(self.samplesCount):
      for l in range(k+1):
        self.similaritiesMatrix[k, l] = self.calculateSimilarity(k, l)
        self.similaritiesMatrix[l, k] = self.similaritiesMatrix[k, l]
      assert abs(self.similaritiesMatrix[k, k] - 1.0) < 1e-10
  
  """Calculate unknown similarity"""
  def calculateSimilarity(self, k, l):
    subsimilarities = np.array([ \
        self.featureSupportById[j].similarity(self.extractedData[k][j], self.extractedData[l][j]) \
          for j in range(self.featuresCount)
      ], dtype=np.float64)
    return np.dot(self.weights, subsimilarities)
  
  """Get precalculated similarity"""
  def similarity(self, k, l):
    return self.similaritiesMatrix[k, l]

