from typing import Set

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

base_lex = '''
:- Program, Create, Range, Int, CondPrefix, CondSuffix, CreatePart

CondSuffix :: CreatePart\\CreatePart
CondPrefix :: Create/CreatePart

create => Program/Create {\\x.program(x)}
list => CreatePart/Range {\\x.list(x)}
from => Range[from]/Int {\\x.x} 
to => (Range\\Range[from])/Int {\\y x.(MIN(x) & MAX(y))}
to => Range/Int {\\x.x} 

even => CondPrefix {\\x.even(x)}
even => CondSuffix {\\x.even(x)}
odd => CondPrefix {\\x.odd(x)}
odd => CondSuffix {\\x.odd(x)}
prime => CondPrefix {\\x.prime(x)}
prime => CondSuffix {\\x.prime(x)}
bigger => CondSuffix/Int {\\y x.bigger(y, x)}
'''


def generate_lex(integers: Set[int]) -> CCGLexicon:
    int_rules = '\n'.join([f"{x} => Int {{{x}}}" for x in integers])
    lex = base_lex + '\n' + int_rules
    print(lex)
    return lexicon.fromstring(lex, True)


base_lexicon = lexicon.fromstring(base_lex, True)
words = set(base_lexicon._entries.keys())


def parse(sentence):
    formatted, numbers = format_sentence(sentence, words, keep_unknown=False)
    print(formatted)
    lex = generate_lex(set(numbers))
    parser = chart.CCGChartParser(lex, chart.DefaultRuleSet)
    result = parser.parse(formatted)
    for parse in result:
        chart.printCCGDerivation(parse)
        break


parse("create even list from 10 to 100 that is odd and bigger than 5")
