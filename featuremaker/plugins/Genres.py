#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class Genres(Feature):
  description = """
Genre: set
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    A = sorted([g['name'] for g in m.genres])
    return ','.join(A)
