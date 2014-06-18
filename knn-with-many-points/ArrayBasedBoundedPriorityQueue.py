#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from BoundedPriorityQueue import *

class ArrayBasedBoundedPriorityQueue(BoundedPriorityQueue):
  """
     k -- maximum size of the queue (only k best elementes are held)
     array -- list of elements
  """
  
  def __init__(self, k):
    BoundedPriorityQueue.__init__(self, k)
    self.array = []
  
  def fix(self):
    for i in range(len(self.array) - 1, 0, -1):
      if self.array[i] < self.array[i-1]:
        self.array[i], self.array[i-1] = self.array[i-1], self.array[i]
      else:
        break
  
  def push(self, element):
    if len(self.array) < self.k:
      self.array.append(element)
      self.fix()
    elif element < self.array[-1]:
      self.array[-1] = element
      self.fix()
  
  def getArray(self):
    return self.array[:]
