#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Feature import Feature
from Stemmer import Stemmer
from unidecode import unidecode

class Overview(Feature):
  description = """
Basic: Overview
""".strip()

  def __init__(self, *args, **kwargs):
    Feature.__init__(self)
    self.stemmer = Stemmer('english')
    self.goodChars = frozenset('abcdefghjiklmnopqrstuvwxyz0123456789')
    self.stopList = frozenset(['a', 'abaft', 'aboard', 'about', 'abov', 'absent', 'accord', 'account', 'across', 'addit', 'afor', 'after', 'against', 'ago', 'ahead', 'all', 'along', 'alongsid', 'alreadi', 'also', 'am', 'amid', 'amidst', 'among', 'amongst', 'an', 'and', 'anenst', 'ani', 'anoth', 'anybodi', 'anyhow', 'anyon', 'anyth', 'anywher', 'apart', 'apr', 'april', 'apropo', 'apud', 'are', 'around', 'as', 'asid', 'astrid', 'at', 'athwart', 'atop', 'aug', 'august', 'back', 'bad', 'bar', 'be', 'becaus', 'been', 'befor', 'begin', 'behalf', 'behest', 'behind', 'below', 'beneath', 'besid', 'best', 'better', 'between', 'beyond', 'big', 'bigger', 'biggest', 'billion', 'blah', 'bln', 'both', 'but', 'by', 'c', 'ca', 'call', 'can', 'cannot', 'cant', 'case', 'circa', 'close', 'concern', 'could', 'couldt', 'current', 'daili', 'day', 'dec', 'decemb', 'despit', 'did', 'do', 'doe', 'doesnt', 'done', 'dont', 'down', 'due', 'dure', 'each', 'eight', 'eighteen', 'eighth', 'eighti', 'eleven', 'end', 'enough', 'ever', 'except', 'exclud', 'fail', 'far', 'feb', 'februari', 'few', 'fifth', 'first', 'five', 'fiveteen', 'fivti', 'follow', 'for', 'forenenst', 'four', 'fourteen', 'fourth', 'fourti', 'fri', 'friday', 'from', 'front', 'full', 'further', 'get', 'given', 'go', 'gone', 'goot', 'had', 'hadnt', 'has', 'hasnt', 'have', 'havent', 'he', 'her', 'here', 'herself', 'high', 'higher', 'hightst', 'himself', 'his', 'how', 'hunderd', 'i', 'if', 'in', 'includ', 'insid', 'instead', 'into', 'is', 'it', 'itself', 'jan', 'januari', 'jul', 'juli', 'jun', 'june', 'just', 'last', 'late', 'later', 'latest', 'left', 'lest', 'lieu', 'like', 'littl', 'long', 'low', 'lower', 'lowest', 'made', 'make', 'mani', 'mar', 'march', 'may', 'me', 'mean', 'mid', 'midst', 'might', 'milliard', 'million', 'mine', 'minus', 'mld', 'mln', 'modulo', 'mon', 'monday', 'month', 'more', 'most', 'mth', 'much', 'must', 'my', 'myself', 'near', 'need', 'neednt', 'neither', 'never', 'next', 'nine', 'nineteen', 'nineth', 'nineti', 'no', 'none', 'nor', 'not', 'notwithstand', 'nov', 'novemb', 'number', 'o', 'oct', 'octob', 'of', 'off', 'on', 'one', 'onli', 'onto', 'oppos', 'opposit', 'or', 'order', 'other', 'ought', 'our', 'ourselv', 'out', 'outsid', 'over', 'owe', 'pace', 'past', 'per', 'place', 'plus', 'point', 'previous', 'prior', 'pro', 'pursuant', 'put', 'qua', 'rather', 'recent', 'regard', 'regardless', 'respect', 'right', 'round', 'said', 'sake', 'same', 'san', 'sat', 'saturday', 'save', 'saw', 'say', 'second', 'see', 'seen', 'sep', 'septemb', 'seven', 'seventeen', 'seventh', 'seventi', 'sever', 'shall', 'she', 'should', 'shouldnt', 'show', 'shown', 'sinc', 'six', 'sixteen', 'sixth', 'sixti', 'small', 'smaller', 'smallest', 'so', 'some', 'somebodi', 'somehow', 'someon', 'someth', 'somewher', 'soon', 'sooner', 'spite', 'start', 'still', 'subsequ', 'such', 'sun', 'sunday', 'take', 'taken', 'tell', 'ten', 'tenth', 'than', 'thank', 'that', 'the', 'their', 'them', 'themselv', 'there', 'these', 'they', 'third', 'thirteen', 'thirti', 'this', 'those', 'thousand', 'three', 'through', 'throughout', 'thru', 'thruout', 'thu', 'thursday', 'till', 'time', 'to', 'today', 'told', 'too', 'took', 'top', 'toward', 'tue', 'tuesday', 'twelv', 'twenti', 'two', 'under', 'underneath', 'unit', 'unlik', 'until', 'unto', 'up', 'upon', 'us', 'use', 'versus', 'via', 'vice', 'view', 'virtu', 'vis', 'visavi', 'vs', 'was', 'we', 'wed', 'wednesday', 'week', 'well', 'went', 'were', 'what', 'when', 'where', 'whether', 'whi', 'which', 'while', 'who', 'whose', 'will', 'with', 'within', 'without', 'wont', 'wors', 'worst', 'worth', 'would', 'wrt', 'xor', 'year', 'yes', 'yesterday', 'yet', 'you', 'your', 'yourself', 'yourselv', 'yr'])
  
  def preprocess(self, s):
    chars = []
    for c in unidecode(s.strip().lower()):
      if c in self.goodChars:
        chars.append(c)
    word = ''.join(chars)
    return self.stemmer.stemWord(word)
  
  def extract(self, m):
    t = m.overview
    return ','.join(sorted(list(set(filter(lambda w: len(w) > 0 and w not in self.stopList, map(self.preprocess, t.split()))))))
