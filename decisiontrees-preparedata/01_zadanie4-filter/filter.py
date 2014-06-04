#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

chosenFeatures = frozenset(filter(None, map(lambda l: l.strip(), open('chosen.csv', 'rt').readlines())))

newFeatureId = 1

featureIdMapping = {}

featureOut = open('output/feature.csv', 'wt')

for line in filter(None, map(lambda l: l.strip(), open('feature.csv', 'rt'))):
  words = list(map(lambda w: w.strip(), line.split(';')))
  oldFeatureId = int(words[0])
  featureName = words[1]
  if featureName not in chosenFeatures: continue
  featureIdMapping[oldFeatureId] = newFeatureId
  featureOut.write('%d;%s\n' % (newFeatureId, featureName))
  newFeatureId += 1

featureOut.close()

entryId = 1

dataOut = open('output/data.csv', 'wt')

for line in filter(None, map(lambda l: l.strip(), open('data.csv', 'rt'))):
  words = list(map(lambda w: w.strip(), line.split(';')))
  userId = int(words[1])
  oldFeatureId = int(words[2])
  if oldFeatureId not in featureIdMapping: continue
  newFeatureId = featureIdMapping[oldFeatureId]
  value = words[3]
  dataOut.write('%d;%d;%d;%s\n' % (entryId, userId, newFeatureId, value))
  entryId += 1

dataOut.close()
