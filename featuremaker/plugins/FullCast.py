#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class FullCast(Feature):
  description = """
Cast: all
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    return ','.join(c['name'] for c in m.cast)
