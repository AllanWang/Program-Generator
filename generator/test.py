# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 08:49:04 2018

@author: Youngsun Jin
"""

from nltk.ccg import chart, lexicon, CCGLexicon
from generator.formatter import format_sentence

lex = lexicon.fromstring('''
     :- S, NP, N
     She => NP {she}
     has => (S\\NP)/NP {\\x y.have(y, x)}
     a => NP/N {\\P.exists z.P(z)}
     book => N {book}
     ''', True)

parser = chart.CCGChartParser(lex, chart.DefaultRuleSet)
parses = list(parser.parse("She has a book".split()))
print(str(len(parses)) + " parses")

chart.printCCGDerivation(parses[0])