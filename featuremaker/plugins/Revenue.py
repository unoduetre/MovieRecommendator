#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class Revenue(Feature):
  description = """
Basic: Revenue
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    return m.revenue
