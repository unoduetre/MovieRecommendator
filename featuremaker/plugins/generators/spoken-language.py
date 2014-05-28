#!/usr/bin/env python3
# -*- coding: utf-8 -*-

languages = [
('en', 'English'),
('fr', 'French'),
('de', 'German'),
('es', 'Spanish'),
('it', 'Italian'),
('ja', 'Japanese'),
('ru', 'Russian'),
('la', 'Latin'),
('ar', 'Arabic'),
('cn', 'Chinese (with incorrect code)'),
('pl', 'Polish'),
('hi', 'Hindi'),
('el', 'Greek'),
('da', 'Danish'),
('pt', 'Portuguese'),
('he', 'Hebrew'),
('vi', 'Vietnamese'),
('zh', 'Chinese'),
('yi', 'Yiddish'),
('no', 'Norwegian'),
('cs', 'Czech'),
('sv', 'Swedish'),
('hu', 'Hungarian'),
('eo', 'Esperanto'),
('fa', 'Persian'),
('xh', 'Xhosa'),
('zu', 'Zulu'),
('ga', 'Irish'),
('af', 'Afrikaans'),
('ne', 'Nepali'),
('ny', 'Chichewa'),
('ta', 'Tamil'),
('gd', 'Scottish Gaelic'),
('tr', 'Turkish'),
('ur', 'Urdu'),
('th', 'Thai'),
('st', 'Southern Sotho')
]

gc = frozenset(list('abcdefghjiklmnopqrstuvwxyz'))

def fix(s):
  r = []
  b = True
  for c in s:
    if c.lower() in gc:
      if b:
        r.append(c.upper())
        b = False
      else:
        r.append(c)
    else:
      b = True
  return ''.join(r)

for code, language in languages:
  cn = fix(language)
  fn = 'IsLanguage%s.py' % cn
  f = open(fn, 'wt')
  f.write("""#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature

class IsLanguage%s(Feature):
  description = \"\"\"
Regional: Spoken languages: is there %s?
\"\"\".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
 
  def extract(self, m):
    for sl in m.spoken_languages:
      if sl['iso_639_1'] == '%s':
        return True
    return False
""" % (cn, language, code))
  f.close()
