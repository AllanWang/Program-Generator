from nltk.ccg import chart, lexicon, CCGLexicon
from generator.formatter import format_sentence

lex: CCGLexicon = lexicon.fromstring('''
:- Create, Range, Int
create => Create/Range
list => Create\\Create
from => Range[from]/Int
~INT~ => Int
to => (Range\\Range[from])/Int
to => Range/Int
''')

parser = chart.CCGChartParser(lex, chart.DefaultRuleSet)
words = set(lex._entries.keys())


def parse(sentence):
    formatted = format_sentence(sentence, words)
    # print(formatted)
    return parser.parse(formatted)
