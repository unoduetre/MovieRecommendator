#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from CFSolver import CFSolver

def main():
  os.chdir(os.path.dirname(sys.argv[0]))
  
  cfSolver = CFSolver(featuresCount=5, trainFn='./resources/dataset/train.csv')
  
  # cfSolver.solveTask('./resources/dataset/task.csv', './output/task1.csv')



if __name__ == '__main__':
  main()
