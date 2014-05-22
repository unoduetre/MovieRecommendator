#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Feature(object):
  def __init__(self):
    assert len(self.description) < 200
    assert self.description.find(';') == -1
  
  def __call__(self, m):
    ret = self.extract(m)
    if ret == None: ret = 'NULL'
    if type(ret) == bool: ret = str(ret).lower()
    ret = str(ret)
    assert len(ret) < 200
    assert ret.find(';') == -1
    return ret
