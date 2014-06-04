#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import math as m
import numpy as np
import random


"""
data should be numpy.array of booleans, equal size for
each entry in DecisionTree

labels should be meaningful integers, i.e. the lower the
difference between a pair of them, the more similar classes
represented by them are
"""
class DecisionTreeEntry(object):
  def __init__(self, data, label):
    assert type(label) == int
    self.data = data
    self.label = label
  
  def __repr__(self):
    return '<%s|%d>' % (''.join(str(int(d)) for d in self.data), self.label)


class PseudoDecisionTree(object):
  def __init__(self, value):
    self.value = value
  
  def __call__(self, *args):
    return self.value


class DecisionTree(object):
  def __init__(self, entries=[], skipCheck=False):
    entries = entries
    if not skipCheck:
      for i in range(len(entries)):
        for j in range(i):
          if entries[i].label != entries[j].label and (entries[i].data == entries[j].data).all():
            raise Exception('Similar vectors with different labels found.')
    self.prepare(entries)
  
  def prepare(self, entries):
    histDict = {}
    for entry in entries:
      if entry.label in histDict: histDict[entry.label] += 1
      else: histDict[entry.label] = 1
    histogram = sorted(histDict.items())
    if len(histogram) == 1:
      self.mode = 0
      self.value = histogram[0][0]
    else:
      if len(histogram) == 2:
        self.mode = 1
        self.threshold = histogram[0][0] + 1
        countA = histogram[0][1]
      else:
        self.mode = 2
        self.threshold = histogram[0][0]
        countA = 0
        half = len(entries) // 2
        for label, count in histogram:
          if abs(countA + count - half) < abs(countA - half):
            countA += count
            self.threshold = label + 1
          else:
            break
      entriesA, entriesB = [], []
      for entry in entries:
        if entry.label < self.threshold: entriesA.append(entry)
        else: entriesB.append(entry)
      if len(histogram) == 2:
        self.treeA = PseudoDecisionTree(histogram[0][0])
        self.treeB = PseudoDecisionTree(histogram[1][0])
      else:
        self.treeA = DecisionTree(entriesA, skipCheck=True)
        self.treeB = DecisionTree(entriesB, skipCheck=True)
      self.conditionsTree = self.makeConditionsTree(set(range(len(entriesA[0].data))), entriesA, entriesB)
  
  def entropy(self, p, n):
    if p == 0 or n == 0: return 0
    x = p / (p + n)
    y = 1.0 - x
    return -(x * m.log2(x) + y * m.log2(y))
  
  def makeConditionsTree(self, availableFeatures, entriesA, entriesB):
    if len(entriesA) == 0: return False
    if len(entriesB) == 0: return True
    
    a = len(entriesA)
    b = len(entriesB)
    n = a + b
    globalEntropy = self.entropy(a, b)
    bestGain = float('-inf')
    bestRoots = []
    
    for feature in availableFeatures:
      a0, a1 = 0, 0
      for entry in entriesA:
        if entry.data[feature] == 0: a0 += 1
        else: a1 += 1
      b0, b1 = 0, 0
      for entry in entriesB:
        if entry.data[feature] == 0: b0 += 1
        else: b1 += 1
      z, o = a0 + b0, a1 + b1
      gain = globalEntropy - ((z / n) * self.entropy(a0, b0) + (o / n) * self.entropy(a1, b1))
      if gain > bestGain:
        bestGain = gain
        bestRoots = [feature]
      elif gain == bestGain:
        bestRoots.append(feature)
    root = random.choice(bestRoots)
    availableFeatures.discard(root)
    
    entriesA0, entriesA1 = [], []
    for entry in entriesA:
      if entry.data[root] == 0: entriesA0.append(entry)
      else: entriesA1.append(entry)
    
    entriesB0, entriesB1 = [], []
    for entry in entriesB:
      if entry.data[root] == 0: entriesB0.append(entry)
      else: entriesB1.append(entry)
    
    tree0 = self.makeConditionsTree(availableFeatures.copy(), entriesA0, entriesB0)
    tree1 = self.makeConditionsTree(availableFeatures.copy(), entriesA1, entriesB1)
    
    return [root, tree0, tree1]
  
  def __call__(self, data):
    if self.mode == 0:
      return self.value
    else:
      ct = self.conditionsTree
      while type(ct) != bool:
        feature = ct[0]
        if data[feature] == 0: ct = ct[1]
        else: ct = ct[2]
      return self.treeA(data) if ct else self.treeB(data)
  
  def show(self, depth=0):
    if self.mode == 0:
      print('  ' * depth, 'class=%d' % self(None))
    else:
      if self.mode == 1:
        a = ('class=%d' % (self.treeA(None)), None)
        b = ('class=%d' % (self.treeB(None)), None)
      else:
        a = ('class<%d' % (self.threshold), self.treeA)
        b = ('class>=%d' % (self.threshold), self.treeB)
      self.conditionsBasedShow(a, b, self.conditionsTree, depth)
  
  def conditionsBasedShow(self, a, b, ct, depth):
    if type(ct) != bool:
      print('  ' * depth, 'x%d=0:' % (ct[0]+1))
      self.conditionsBasedShow(a, b, ct[1], depth+1)
      print('  ' * depth, 'x%d=1:' % (ct[0]+1))
      self.conditionsBasedShow(a, b, ct[2], depth+1)
    elif ct == True:
      print('  ' * depth, a[0])
      if a[1] != None:
        a[1].show(depth + 1)
    elif ct == False:
      print('  ' * depth, b[0])
      if b[1] != None:
        b[1].show(depth + 1)
  
  def PISIshow(self, fh, prefix='', label='Some decision tree'):
    if prefix == '':
      fh.write('digraph {\n')
      fh.write('label="%s";' % label)
      fh.write('labelloc=top;')
      fh.write('labeljust=left;')
      prefix = 'root'
    if self.mode == 0:
      fh.write('  %s [label="vote=%d",shape="rect"];\n' % (prefix, self(None)))
    else:
      if self.mode == 1:
        a = ('vote=%d' % (self.treeA(None)), None)
        b = ('vote=%d' % (self.treeB(None)), None)
      else:
        a = ('vote<%d' % (self.threshold), self.treeA)
        b = ('vote>=%d' % (self.threshold), self.treeB)
      self.PISIconditionsBasedShow(a, b, self.conditionsTree, fh, prefix)
    if prefix == 'root':
      fh.write('}\n')
  
  def PISIconditionsBasedShow(self, a, b, ct, fh, prefix):
    if prefix == 'root':
      aprefix = 'A'
      bprefix = 'B'
    else:
      aprefix = prefix + 'A'
      bprefix = prefix + 'B'
    if type(ct) != bool:
      fh.write('  %s [label="feature#%d"];\n' % (prefix, ct[0]+1))
      self.PISIconditionsBasedShow(a, b, ct[1], fh, aprefix)
      fh.write('  %s -> %s [label="false"];\n' % (prefix, aprefix))
      self.PISIconditionsBasedShow(a, b, ct[2], fh, bprefix)
      fh.write('  %s -> %s [label="true"];\n' % (prefix, bprefix))
    elif ct == True:
      if a[1] != None:
        fh.write('  %s [label="%s",shape="note"];\n' % (prefix, a[0]))
        a[1].PISIshow(fh, aprefix)
        fh.write('  %s -> %s;\n' % (prefix, aprefix))
      else:
        fh.write('  %s [label="%s",shape="rect"];\n' % (prefix, a[0]))
    elif ct == False:
      if b[1] != None:
        fh.write('  %s [label="%s",shape="note"];\n' % (prefix, b[0]))
        b[1].PISIshow(fh, bprefix)
        fh.write('  %s -> %s;\n' % (prefix, bprefix))
      else:
        fh.write('  %s [label="%s",shape="rect"];\n' % (prefix, b[0]))
  