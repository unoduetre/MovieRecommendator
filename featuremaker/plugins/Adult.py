#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class Adult(Feature):
  description = """
Basic: Adult
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    return m.adult
