#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import math as m
import random
import importlib.machinery

os.chdir(os.path.dirname(sys.argv[0]))


def main():
  featuresInFn = 'resources/zadanie3/feature.csv'
  dataInFn = 'resources/zadanie3/data.csv'
  featuresOutFn = 'output/zadanie3/feature.csv'
  dataOutFn = 'output/zadanie3/data.csv'
  
  """featuresInFn = 'resources/zadanie4/feature.csv'
  dataInFn = 'resources/zadanie4/data.csv'
  featuresOutFn = 'output/zadanie4/feature.csv'
  dataOutFn = 'output/zadanie4/data.csv'"""
  
  featureIdsByName = {}
  for line in filter(None, map(lambda l: l.strip(), open(featuresInFn, 'rt'))):
    words = list(map(lambda w: w.strip(), line.split(';')))
    featureName = words[1]
    featureId = int(words[0])-1 # for 0-indexing
    featureIdsByName[featureName] = featureId
  
  featuresCount = len(featureIdsByName)
  featureNamesById = [None for _ in range(featuresCount)]
  for featureName, featureId in featureIdsByName.items():
    featureNamesById[featureId] = featureName
  
  data = []
  for l in filter(None, map(lambda l: l.strip(), open(dataInFn, 'rt').readlines())):
    w = l.split(';')
    movieId = int(w[1])-1 # for 0-indexing
    featureId = int(w[2])-1 # for 0-indexing
    featureValue = w[3]
    if movieId >= len(data): data.append([None for _ in range(featuresCount)])
    data[movieId][featureId] = featureValue
  assert sum(row.count(None) for row in data) == 0
  
  featureBooleanizersByName = {}
  for pluginFileBasename in os.listdir('plugins'):
    if not pluginFileBasename.endswith('.py'): continue
    pluginFn = os.path.join('plugins', pluginFileBasename)
    name = pluginFileBasename[:-3]
    loader = importlib.machinery.SourceFileLoader(name, pluginFn)
    module = loader.load_module()
    for featureName, featureBooleanizer in module.featureBooleanizersByName.items():
      if featureName in featureIdsByName:
        featureId = featureIdsByName[featureName]
        featureBooleanizersByName[featureName] = featureBooleanizer(featureName, data, featureId)
  
  for featureName in featureIdsByName:
    assert featureName in featureBooleanizersByName
  
  featuresOutFile = open(featuresOutFn, 'wt')
  newFeatureId = 0
  for featureId, featureName in enumerate(featureNamesById):
    for newFeatureName in featureBooleanizersByName[featureName].getFeatureNames():
      featuresOutFile.write('%d;%s\n' % (newFeatureId+1, newFeatureName))
      newFeatureId += 1
  featuresOutFile.close()
  newFeaturesCount = newFeatureId
  
  entryId = 0
  dataOutFile = open(dataOutFn, 'wt')
  for movieId in range(len(data)):
    newFeatureId = 0
    for featureId, featureName in enumerate(featureNamesById):
      for newFeatureValue in featureBooleanizersByName[featureName].process(data[movieId][featureId]):
        dataOutFile.write('%d;%d;%d;%s\n' % (entryId+1, movieId+1, newFeatureId+1, 'true' if newFeatureValue else 'false'))
        newFeatureId += 1
        entryId += 1
  dataOutFile.close()
  
  

if __name__ == '__main__':
  main()
