#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class Popularity(Feature):
  description = """
Basic: Popularity
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    return m.popularity
