#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from FeatureSupport import *

class BooleanFeatureSupport(FeatureSupport):
  def __init__(self, featuresData, featureId):
    FeatureSupport.__init__(self, featuresData, featureId)
  
  def extract(self, i):
    assert self[i] in ('true', 'false')
    return self[i] == 'true'
  
  def similarity(self, a, b):
    return float(a == b)


featureSupportLoadersByName = {}

for genreName in ('action movie', 'adventure movie', 'animation', 'comedy', 'crime movie', 'drama', 'family movie', 'fantasy', 'film noir', 'history movie', 'horror', 'mystery movie',
'romance', 'science fiction', 'suspense movie', 'thriller', 'war movie', 'western'):
  featureName = 'Genre: is it %s?' % genreName
  featureSupportLoadersByName[featureName] = BooleanFeatureSupport

for country in ('France', 'Germany', 'UK', 'USA'):
  featureName = 'Regional: Production country: is it %s?' % country
  featureSupportLoadersByName[featureName] = BooleanFeatureSupport

for language in ('English', 'French', 'German', 'Italian', 'Japanese', 'Latin', 'Russian', 'Spanish'):
  featureName = 'Regional: Spoken languages: is there %s?' % language
  featureSupportLoadersByName[featureName] = BooleanFeatureSupport

