#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class FeatureBooleanizer(object):
  def __init__(self, featureName, featuresData, featureId):
    self.featuresData = featuresData
    self.featureId = featureId
    self.featureName = featureName
  
  def getFeatureNames(self):
    return [self.featureName]
  
  def process(self, v):
    return [bool(v)]
