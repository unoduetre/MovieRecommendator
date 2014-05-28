#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from FeaturesData import FeaturesData
from VoteGuesser import VoteGuesser

def main():
  os.chdir(os.path.dirname(sys.argv[0]))
  
  """Zadanie 3."""
  """
  featuresData = FeaturesData(featuresFn='./resources/features-zadanie3/feature.csv',
                              dataFn='./resources/features-zadanie3/data.csv',
                              weightsFn='./resources/features-zadanie3/weight-manual.csv')
  voteGuesser = VoteGuesser(featuresData, k=3)
  
  print('Average error:', voteGuesser.calculateReguessExpectedError())
  voteGuesser.solveTask(outputFn='./output/zadanie3/task.csv')
  """
  
  """Zadanie 4."""
  featuresData = FeaturesData(featuresFn='./resources/features-zadanie4/feature.csv',
                              dataFn='./resources/features-zadanie4/data.csv',
                              weightsFn='./resources/features-zadanie4/weight.csv')
  voteGuesser = VoteGuesser(featuresData, k=3)
  
  print('Average error for all features:', voteGuesser.calculateReguessExpectedError())
  voteGuesser.solveTask(outputFn='./output/zadanie4/task1.csv')
  
  voteGuesser.loadMask(maskFn='./output/zadanie4/mask.csv')
  print('Average error for selected features:', voteGuesser.calculateReguessExpectedError())
  voteGuesser.solveTask(outputFn='./output/zadanie4/task2.csv')

if __name__ == '__main__':
  main()
