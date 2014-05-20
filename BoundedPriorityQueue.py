#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class BoundedPriorityQueue(object):
  def __init__(self, k):
    assert type(k) == int and k > 0
    self.k = k
  
  """i -- number of row in raw self.featuresData.data"""
  def push(self, element):
    raise Exception('Implementation not provided, template called.')
  
  """get resulting sorted array"""
  def getArray(self):
    raise Exception('Implementation not provided, template called.')
    return [None for _ in range(k)]
