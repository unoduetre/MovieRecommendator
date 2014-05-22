#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class Producer(Feature):
  description = """
Crew: the first movie producer
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for c in m.crew:
      if c['job'] == 'Producer':
        return c['name']
