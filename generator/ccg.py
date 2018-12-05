from typing import Set, Optional

import nltk
from nltk.ccg import chart, lexicon, CCGLexicon
from generator.formatter import format_sentence

base_lex = '''
:- Program, Create, Range, Int, CondPrefix, CondSuffix

CondPrefix :: Create[pre]/Create[pre]
CondSuffix :: Create[post]\\Create

create => Program/Create {\\x.program(x)}
list => Create[pre]/Range {\\x.list(x)}
from => Range[from]/Int {\\x.x} 
to => (Range\\Range[from])/Int {\\y x.R(x,y)}
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
    """
    Given integer set, add them to the base lex to create the new parser.
    For base_lex, note that in lists, conditions before the list take precendence
    over conditions after the list
    """
    int_rules = '\n'.join([f"{x} => Int {{{x}}}" for x in integers])
    lex = base_lex + '\n' + int_rules
    return lexicon.fromstring(lex, True)


words = set([w.split("=>")[0].strip() for w in base_lex.split("\n") if "=>" in w])


def parse(sentence: str) -> Optional[nltk.Tree]:
    formatted, numbers = format_sentence(sentence, words, keep_unknown=False)
    lex = generate_lex(set(numbers))
    parser = chart.CCGChartParser(lex, chart.DefaultRuleSet)
    results = parser.parse(formatted)
    return next(results, None)


def test(sentence):
    result = parse(sentence)
    if result:
        chart.printCCGDerivation(result)
    else:
        print("No result found")


test("create even list from 0 to 100 that is bigger than 5")
