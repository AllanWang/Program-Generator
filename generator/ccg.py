from nltk.ccg import chart, lexicon, CCGLexicon
from formatter import format_sentence

lex: CCGLexicon = lexicon.fromstring('''
:- Create, Range, Int, Cond
create => Create/Range {\\x.create(x)}
list => Create\\Create {\\x.x}
from => Range[from]/Int {\\x.x} 
~INT~ => Int {~NUM~}
to => (Range\\Range[from])/Int {\\y x.(MIN(x) & MAX(y))}
to => Range/Int {\\x.x} 
''', True)


parser = chart.CCGChartParser(lex, chart.DefaultRuleSet)
words = set(lex._entries.keys())

def parse(sentence):
    
    formatted = format_sentence(sentence, words)
    print(formatted)
    result = parser.parse(formatted)
    for parse in result:
        chart.printCCGDerivation(parse)
        break

parse("create list from 0 to 100")