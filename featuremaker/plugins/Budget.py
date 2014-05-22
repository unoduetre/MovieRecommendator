#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class Budget(Feature):
  description = """
Basic: Budget
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    return m.budget
