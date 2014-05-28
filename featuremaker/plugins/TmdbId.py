#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class TmdbId(Feature):
  description = """
Helpers: TMDB Id
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    return m.tmdbId
