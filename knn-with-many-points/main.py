#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import pickle
from FeaturesData import FeaturesData
from UsersData import UsersData
from CombinedData import CombinedData
from VoteGuesser import VoteGuesser

def main():
  os.chdir(os.path.dirname(sys.argv[0]))
  
  if not os.path.exists('./pickles/features-data.pickle'):
    featuresDataFile = open('./pickles/features-data.pickle', 'wb')
    featuresData = FeaturesData()
    featuresData.loadMask(maskFn='./resources/features/mask.csv')
    pickle.dump(featuresData, featuresDataFile)
    featuresDataFile.close()
  else:
    featuresDataFile = open('./pickles/features-data.pickle', 'rb')
    featuresData = pickle.load(featuresDataFile)
    featuresDataFile.close()
  
  if not os.path.exists('./pickles/users-data.pickle'):
    usersDataFile = open('./pickles/users-data.pickle', 'wb')
    usersData = UsersData()
    pickle.dump(usersData, usersDataFile)
    usersDataFile.close()
  else:
    usersDataFile = open('./pickles/users-data.pickle', 'rb')
    usersData = pickle.load(usersDataFile)
    usersDataFile.close()
  
  combinedData = CombinedData(featuresData, usersData)
  voteGuesser = VoteGuesser(combinedData, k=3)
  
  print('Average error:', voteGuesser.calculateReguessExpectedError())
  print('Tested weights', combinedData.weights)


if __name__ == '__main__':
  main()
