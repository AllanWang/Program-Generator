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
:- Create, Range, Int, Cond, CondInd
CondInd :: Create\\Create {\\x.x}
create => Create/Range {\\x.create(x)}
list => Create\\Create {\\x.x}
from => Range[from]/Int {\\x.x} 
~INT~ => Int {~NUM~}
to => (Range\\Range[from])/Int {\\y x.(MIN(x) & MAX(y))}
to => Range/Int {\\x.x} 
even => CondInd {\\x.x}
''', True)

parser = chart.CCGChartParser(lex, chart.DefaultRuleSet)
words = set(lex._entries.keys())

def parse(sentence):
    
    formatted = format_sentence(sentence, words, keep_unknown=False)
    print(formatted)
    result = parser.parse(formatted)
    for parse in result:
        chart.printCCGDerivation(parse)
        break

parse("create list from 0 to 100 that is even")