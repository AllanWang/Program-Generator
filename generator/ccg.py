from nltk.ccg import chart, lexicon, CCGLexicon
from generator.formatter import format_sentence

# lex: CCGLexicon = lexicon.fromstring('''
# :- S, Create, List, Range, Int, CondInd, Cond, CondBranch, Conj
# Create :: S
# CondBranch :: S\\Create\\Conj
# CondInd :: List/List
# Cond :: Create\\Create
# Range :: S
#
# create => Create/List/Range
# create => (Create\\Range)/List
# list => List
# from => Range[from]/Int
# ~INT~ => Int
# to => (Range\\Range[from])/Int
# even => CondInd
# bigger => Cond/Int
# if => CondBranch/Cond
# and => Conj
# ''')

lex: CCGLexicon = lexicon.fromstring('''
:- S, NP, N
the => NP/N
dog => N
john => NP
bit => (S\\NP)/NP
''')

parser = chart.CCGChartParser(lex, chart.DefaultRuleSet)
words = set(lex._entries.keys())


def parse(sentence):
    formatted = format_sentence(sentence, words)
    # print(formatted)
    return parser.parse(formatted)
