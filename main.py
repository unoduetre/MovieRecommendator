#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from FeaturesData import FeaturesData
from VoteGuesser import VoteGuesser

def main():
  os.chdir(os.path.dirname(sys.argv[0]))

  featuresData = FeaturesData()
  voteGuesser = VoteGuesser(featuresData, k=3)
  voteGuesser.solveTask()
  voteGuesser.printReport()


if __name__ == '__main__':
  main()
