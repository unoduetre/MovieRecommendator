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
  
  
  """Load plugins"""
  def loadFeaturePlugins(self):
    self.featureSupportByName = {}
    for pluginFileBasename in os.listdir('plugins'):
      if (not pluginFileBasename.endswith('.py')) or pluginFileBasename.startswith('__'): continue
      pluginFn = os.path.join('plugins', pluginFileBasename)
      name = 'plugins.'+pluginFileBasename[:-3]
      loader = importlib.machinery.SourceFileLoader(name, pluginFn)
      module = loader.load_module()
      for featureName, featureSupportLoader in module.featureSupportLoadersByName.items():
        if featureName in self.featureIdsByName:
          assert featureName not in self.featureSupportByName
          featureId = self.featureIdsByName[featureName]
          self.featureSupportByName[featureName] = featureSupportLoader(self, featureId)
    
    for k in self.featureIdsByName:
      if k not in self.featureSupportByName:
        print(k)
    
    for k in self.featureIdsByName: assert k in self.featureSupportByName
    
    self.featureSupportById = [None for _ in range(self.featuresCount)]
    for featureName, featureSupport in self.featureSupportByName.items():
      featureId = self.featureIdsByName[featureName]
      self.featureSupportById[featureId] = featureSupport
  
  
  """Extract features from raw data"""
  def performFeatureExtraction(self):
    self.extractedData = []
    for i, row in enumerate(self.data):
      self.extractedData.append([None for _ in range(self.featuresCount)])
      for j in range(self.featuresCount):
        self.extractedData[i][j] = self.featureSupportById[j].extract(i)
  
  
  """Load weights"""
  def loadFeatureWeights(self, weightsFn):
    self.weights = np.empty(self.featuresCount, dtype=np.float64)
    if weightsFn != None:
      self.weights.fill(-1.0)
      for l in filter(None, map(lambda l: l.strip(), open(weightsFn, 'rt').readlines())):
        w = l.split(';')
        featureName = w[0]
        featureId = self.featureIdsByName[featureName]
        weight = float(w[1])
        self.weights[featureId] = weight
    else:
      self.weights.fill(1.0)
    self.normalizeWeights()
    assert np.min(self.weights) >= 0.0
    assert abs(np.sum(self.weights) - 1.0) < 1e-10
  
  
  """"""
  def getFeatureGroups(self):
    groupPrefixes = ['Genre: is it', 'Regional: Production country: is it', 'Regional: Spoken languages: is there']
    featureGroups = [[] for prefix in groupPrefixes]
    for featureId in range(self.featuresCount):
      featureName = self.featureNamesById[featureId]
      groupId = None
      for prefixId, prefix in enumerate(groupPrefixes):
        if featureName.startswith(prefix):
          groupId = prefixId
          break
      if groupId == None:
        featureGroups.append([featureId])
      else:
        featureGroups[groupId].append(featureId)
    return featureGroups
  
  
  """"""
  def calculateSubsimilarity(self, k, l, featureId):
    return self.featureSupportById[featureId].similarity(self.extractedData[k][featureId], self.extractedData[l][featureId])
  
  
  """Calculate subsimilarities"""
  def calculateSubsimilarities(self, k, l):
    return np.array([self.calculateSubsimilarity(k, l, featureId) for featureId in range(self.featuresCount)], dtype=np.float64)
  
  
  """Calculate unknown similarity"""
  def calculateSimilarity(self, k, l):
    return np.dot(self.weights, self.calculateSubsimilarities(k, l))
  
  
  """Precalculate subsimilarities matrix"""
  def prepareSubsimilaritiesMatrix(self):
    self.subsimilaritiesMatrix = np.empty([self.samplesCount, self.samplesCount, self.featuresCount], dtype=np.float64)
    for featureId in range(self.featuresCount):
      for k in range(self.samplesCount):
        for l in range(k+1):
          self.subsimilaritiesMatrix[k, l, featureId] = self.calculateSubsimilarity(k, l, featureId)
          self.subsimilaritiesMatrix[l, k, featureId] = self.subsimilaritiesMatrix[k, l, featureId]
        assert abs(self.subsimilaritiesMatrix[k, k, featureId] - 1.0) < 1e-10
  
  
  """Precalculate similarities matrix"""
  def prepareSimilaritiesMatrix(self):
    self.similaritiesMatrix = np.empty([self.samplesCount, self.samplesCount], dtype=np.float64)
    for k in range(self.samplesCount):
      for l in range(k+1):
        self.similaritiesMatrix[k, l] = np.dot(self.weights * self.mask, self.subsimilaritiesMatrix[k, l])
        self.similaritiesMatrix[l, k] = self.similaritiesMatrix[k, l]
  
  
  """Get precalculated similarity"""
  def similarity(self, k, l):
    return self.similaritiesMatrix[k, l]
  
  
  """Normalize weights (important before calculating similarities)"""
  def normalizeWeights(self):
    self.weights /= sum(self.weights)
  
  
  """Make all the weights equal"""
  def resetWeights(self):
    self.weights.fill(1.0)
    self.normalizeWeights()
  
  
  """Create new weight.csv"""
  def serializeWeights(self, outWeightsFn='./output/weight.csv'):
    f = open(outWeightsFn, 'wt')
    for featureId in range(self.featuresCount):
      f.write('%s;%s\n' % (self.featureNamesById[featureId], '{0:.16f}'.format(self.weights[featureId])))
    f.close()
  
  
  """Serialize masks"""
  def serializeMask(self, outMaskFn='./output/mask.csv'):
    f = open(outMaskFn, 'wt')
    for featureId in range(self.featuresCount):
      f.write('%s;%s\n' % (self.featureNamesById[featureId], str(self.mask[featureId]).lower()))
    f.close()
   
  
  """Load mask"""
  def loadMask(self, maskFn='./resources/mask.csv'):
    self.mask.fill(False)
    for l in filter(None, map(lambda l: l.strip(), open(maskFn, 'rt').readlines())):
      w = l.split(';')
      featureName = w[0]
      featureId = self.featureIdsByName[featureName]
      value = w[1].strip().lower() == 'true'
      self.mask[featureId] = value
    self.weights /= np.dot(self.weights, self.mask)
    self.prepareSimilaritiesMatrix()
