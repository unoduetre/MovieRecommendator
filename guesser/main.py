#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from FeaturesData import FeaturesData
from VoteGuesser import VoteGuesser

def main():
  os.chdir(os.path.dirname(sys.argv[0]))

  featuresData = FeaturesData()
  # voteGuesser = VoteGuesser(featuresData, k=3, trainFn='./resources/our-votes/train.csv', taskFn='./resources/our-votes/task.csv')
  voteGuesser = VoteGuesser(featuresData, k=3)
  voteGuesser.solveTask()
  # voteGuesser.printSimilarityReport()
  # voteGuesser.printReguessReport()
  
  """A = []
  for movieId in range(featuresData.samplesCount):
    A.append(float(featuresData.data[movieId][-2]))
  
  print(min(A), max(A))"""
  
  """userId = 3 # 1642
  refMovieId = 113-1 # 137-1
  
  for otherMovieId, vote in sorted(voteGuesser.userData[userId].items(), key=lambda t: t[1]):
    sss = '\n\t'.join('%.2f %12s %s' % (x, featuresData.data[otherMovieId][i], featuresData.featureNamesById[i]) for i, x in enumerate(featuresData.calculateSubsimilarities(refMovieId, otherMovieId)))
    print(otherMovieId, vote, featuresData.similarity(refMovieId, otherMovieId), '\n\t'+ sss)"""
  
  """arr = []
  for i in range(featuresData.samplesCount):
    for j in range(featuresData.samplesCount):
      if i == j: break
      arr.append((featuresData.similarity(i, j), i+1, j+1))
  arr.sort()
  print(arr[:5])
  print(arr[-5:])"""

if __name__ == '__main__':
  main()
