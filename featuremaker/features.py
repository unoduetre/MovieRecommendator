#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import pickle
import importlib.machinery
from tmdbsimple import TMDB

os.chdir(os.path.dirname(sys.argv[0]))

tmdb = TMDB('f75fcb1e6965192e9ad5c473a8e9728a')

class Movie(object):
  def __init__(self, movieId, tmdbId):
    self.movieId = movieId
    self.tmdbId = tmdbId
    tmdbMovie = tmdb.Movies(tmdbId)
    tmdbMovie.info()
    tmdbMovie.credits()
    for attr in ['adult', 'belongs_to_collection', 'budget', 'cast', 'crew', 'genres', 'original_title', 'overview', 'popularity', 'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'tagline', 'title', 'vote_average', 'vote_count']:
      setattr(self, attr, getattr(tmdbMovie, attr))
    self.keywords = tmdbMovie.keywords()['keywords']
    self.similar_movies = tmdbMovie.similar_movies()['results']
    self.reviews = tmdbMovie.reviews()['results']
  
  def __repr__(self):
    return 'Movie<pisi#%d,tmdb#%d>' % (self.movieId, self.tmdbId)

class Person(object):
  def __init__(self, tmdbId):
    self.tmdbId = tmdbId
    tmdbPerson = tmdb.People(tmdbId)
    tmdbPerson.info()
    for attr in ['adult', 'biography', 'birthday', 'deathday', 'name', 'place_of_birth', 'popularity']:
      setattr(self, attr, getattr(tmdbPerson, attr))

if not os.path.exists('movies.pickle'):
  movies = []
  for line in open('movies.csv', 'rt'):
    line = line.strip()
    if not line: continue
    movieId, tmdbId = map(int, line.split(';')[:2])
    m = Movie(movieId, tmdbId)
    movies.append(m)
    print(m.title)
  f = open('movies.pickle', 'wb')
  pickle.dump(movies, f)
  f.close()
else:
  f = open('movies.pickle', 'rb')
  movies = pickle.load(f)
  f.close()

persons = {}

if not os.path.exists('persons.pickle'):
  pids = set()
  for m in movies:
    for p in m.cast:
      pids.add(p['id'])
    for p in m.crew:
      pids.add(p['id'])
  for pid in pids:
    persons[pid] = Person(pid)
    print(persons[pid].name, len(persons), len(pids))
  f = open('persons.pickle', 'wb')
  pickle.dump(persons, f)
  f.close()
else:
  f = open('persons.pickle', 'rb')
  persons = pickle.load(f)
  f.close()

plugins = []

for pfbn in os.listdir('plugins'):
  if not pfbn.endswith('.py'): continue
  if pfbn == 'Feature.py': continue
  pfn = os.path.join('plugins', pfbn)
  name = pfbn[:-3]
  loader = importlib.machinery.SourceFileLoader(name, pfn)
  module = loader.load_module()
  plugin = getattr(module, name)(tmdb=tmdb, movies=movies, persons=persons)
  plugins.append(plugin)

plugins.sort(key=lambda p: p.description.lower())

ff = open('out/feature.csv', 'wt')
for i in range(len(plugins)):
  ff.write('%d;%s\n' % (i+1, plugins[i].description))
ff.close()

df = open('out/data.csv', 'wt')
ii = 0
for m in movies:
  for i in range(len(plugins)):
    df.write('%d;%d;%d;%s\n' % (ii+1, m.movieId, i+1, plugins[i](m)))
    ii += 1
df.close()

def mkhist(l):
  hist = {}
  for m in movies:
    for n in l(m):
      if n not in hist: hist[n] = 1
      else: hist[n] += 1
  for n, c in sorted(hist.items(), key=lambda t:-t[1]):
    print(n, c)

# mkhist(lambda m: list(g['name'] for g in m.genres))
# mkhist(lambda m: list(sl['iso_639_1'] for sl in m.spoken_languages))
# mkhist(lambda m: list(pc['iso_3166_1'] for pc in m.production_countries))

# print(movies[174].cast)
