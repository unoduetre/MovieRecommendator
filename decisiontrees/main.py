#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, shutil
import math as m
import time
import random
import numpy as np
import pickle

from DecisionTree import *

os.chdir(os.path.dirname(sys.argv[0]))


def formatTime(t):
  c = int(t * 100 + 0.5) % 100
  s = int(t) % 60
  m = int(t / 60) % 60
  h = int(t / 3600)
  ret = '%d.%.2ds' % (s, c)
  if m: ret = '%dm %s' % (m, ret)
  if h: ret = '%dh %s' % (h, ret)
  return ret


def main():
  """our features"""
  """
  featuresFn = 'resources/zadanie3/feature.csv'
  dataFn = 'resources/zadanie3/data.csv'
  trainFn = 'resources/dataset/train.csv'
  taskFn = 'resources/dataset/task.csv'
  outputFn = 'output/task1.csv'
  graphFn = 'output/task1.dot'
  treesDir = 'output/trees1'
  """
  
  """automatically selected features"""
  """"""
  featuresFn = 'resources/zadanie4/feature.csv'
  dataFn = 'resources/zadanie4/data.csv'
  trainFn = 'resources/dataset/train.csv'
  taskFn = 'resources/dataset/task.csv'
  outputFn = 'output/task2.csv'
  graphFn = 'output/task2.dot'
  treesDir = 'output/trees2'
  """"""
  
  loops = 1
  
  """Read feature.csv"""
  featureIdsByName = {}
  for l in filter(None, map(lambda l: l.strip(), open(featuresFn, 'rt').readlines())):
    w = l.split(';')
    featureId = int(w[0])-1 # for 0-indexing
    featureName = w[1]
    featureIdsByName[featureName] = featureId
  assert tuple(sorted(featureIdsByName.values())) == tuple(range(len(featureIdsByName)))
  featuresCount = len(featureIdsByName)
  
  featureNamesById = [None for _ in range(featuresCount)]
  for featureName, featureId in featureIdsByName.items():
    featureNamesById[featureId] = featureName
  
  """Read data.csv"""
  data = []
  for l in filter(None, map(lambda l: l.strip(), open(dataFn, 'rt').readlines())):
    w = l.split(';')
    movieId = int(w[1])-1 # for 0-indexing
    featureId = int(w[2])-1 # for 0-indexing
    featureValue = (w[3] == 'true')
    if movieId >= len(data):
      data.append(np.empty(featuresCount, dtype=np.bool))
    data[movieId][featureId] = featureValue
  
  """Read train.csv"""
  userData = {}
  for l in filter(None, map(lambda l: l.strip(), open(trainFn, 'rt').readlines())):
    w = l.split(';')
    userId = int(w[1])
    movieId = int(w[2])-1 # for 0-indexing
    vote = int(w[3])
    if userId not in userData: userData[userId] = {}
    userData[userId][movieId] = vote
  
  """Read task.csv"""
  requests = [] # element structure: [pisiId, userId, movieId, listOfResultsFromPotentiallyMultipleDesicionTrees]
  requestsByUser = {}
  for l in filter(None, map(lambda l: l.strip(), open(taskFn, 'rt').readlines())):
    w = l.split(';')
    pisiId = int(w[0])
    userId = int(w[1])
    movieId = int(w[2])-1 # for 0-indexing
    requests.append([pisiId, userId, movieId, []])
    if userId not in requestsByUser:
      requestsByUser[userId] = [len(requests)-1]
    else:
      requestsByUser[userId].append(len(requests)-1)
  
  """Prepare decition tree entries for each user included in the requests"""
  entriesByUser = {}
  for userId in requestsByUser: entriesByUser[userId] = [DecisionTreeEntry(data[movieId], vote) for movieId, vote in userData[userId].items()]
  
  if os.path.exists(treesDir): shutil.rmtree(treesDir)
  os.mkdir(treesDir)
  
  usersDone = 0
  usersTodo = len(requestsByUser) * loops
  graphCreated = False
  t0 = time.time()
  
  for iteration in range(loops):
    """For each user included in the requests, we build a decision tree and solve requests"""
    for userId in requestsByUser:
      print('User %d started.' % (userId))
      dt = DecisionTree(entriesByUser[userId], skipCheck=(iteration != 0))
      for requestId in requestsByUser[userId]:
        movieId = requests[requestId][2]
        requests[requestId][3].append(dt(data[movieId]))
      
      pickleFn = os.path.join(treesDir, 'tree_%d_%d.pickle' % (userId, iteration+1))
      pickleFile = open(pickleFn, 'wb')
      pickle.dump(dt, pickleFile)
      pickleFile.close()
      
      if not graphCreated:
        dotFile = open(graphFn, 'wt')
        dt.PISIshow(dotFile, label='Tree for user #%d (example)' % userId)
        dotFile.close()
        graphCreated = True
      
      print('User %d finished.' % (userId))
      usersDone += 1
      usersTodo -= 1
      avgUserTime = (time.time() - t0) / usersDone
      print('ETA:', formatTime(avgUserTime * usersTodo))
  
  outputFh = open(outputFn, 'wt')
  for pisiId, userId, movieId, dtVotes in requests:
    vote = sorted(dtVotes)[len(dtVotes) // 2] # Unpotimized median, good enough for small collections
    outputFh.write('%d;%d;%d;%d\n' % (pisiId, userId, movieId+1, vote))
  outputFh.close()
  

if __name__ == '__main__':
  main()
