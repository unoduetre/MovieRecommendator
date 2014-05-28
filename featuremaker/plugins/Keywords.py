#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class Keywords(Feature):
  description = """
Basic: Keywords
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    return ','.join(k['name'] for k in m.keywords)
