from typing import Set, Optional

import nltk
from nltk.ccg import chart, lexicon, CCGLexicon

from generator.formatter import Formatter
from generator.node import Node

base_lex = '''
:- Program, Create, Range, Int

CondPrefix :: Create[pre]/Create[pre]
CondSuffix :: Create[post]\\Create

create => Program/Create {\\x.program(x)}
list => Create[pre]/Range[from]/Range[to] {\\y x.list(x, y)}
from => Range[from]/Int {\\x.x} 
to => Range[to]/Int {\\x.x}

not => CondPrefix {\\x.neg(x)}
not => CondSuffix {\\x.neg(x)}
even => CondPrefix {\\x.even(x)}
even => CondSuffix {\\x.even(x)}
odd => CondPrefix {\\x.odd(x)}
odd => CondSuffix {\\x.odd(x)}
# prime => CondPrefix {\\x.prime(x)}
# prime => CondSuffix {\\x.prime(x)}
bigger => CondSuffix/Int {\\y x.bigger(y, x)}
'''

synset_name_pool = {
    'even': 'even.a.01',
    'odd': 'odd.a.01',
    # 'prime': 'prime.n.01',
    'create': 'produce.v.02',
    'list': 'list.n.01',
    'bigger': 'bigger.s.01',
    'from': [],
    'to': []
}

words = set([w.partition("=>")[0].strip() for w in base_lex.split("\n") if "=>" in w])

formatter = Formatter(words, synset_name_pool)


def generate_lex(integers: Set[int]) -> CCGLexicon:
    """
    Given integer set, add them to the base lex to create the new parser.
    For base_lex, note that in lists, conditions before the list take precendence
    over conditions after the list
    """
    int_rules = '\n'.join([f"{x} => Int {{{x}}}" for x in integers])
    lex = base_lex + '\n' + int_rules
    return lexicon.fromstring(lex, True)


def parse(sentence: str, print_warnings: bool = True) -> Optional[nltk.Tree]:
    formatted = formatter.format_sentence(sentence)
    if isinstance(formatted, str):
        if print_warnings:
            print(formatted)
        return None
    formatted_sentence, numbers = formatted
    lex = generate_lex(set(numbers))
    parser = chart.CCGChartParser(lex, chart.DefaultRuleSet)
    results = parser.parse(formatted_sentence)
    return next(results, None)


def tree_to_node(tree: nltk.Tree) -> Node:
    token: nltk.ccg.lexicon.Token = tree.label()[0]
    return Node.parse(str(token.semantics()))


def parse_to_node(sentence: str) -> Optional[Node]:
    tree = parse(sentence)
    if tree is None:
        return None
    return tree_to_node(tree)


def test_formatted():
    formatter = Formatter(synset_name_pool.keys(), synset_name_pool)
    print(formatter._words)
    print(formatter._synonyms)
    print(formatter.format_sentence('even bigger'))


def test_ccg(*sentence: str):
    for s in sentence:
        tree = parse(s)
        if tree:
            chart.printCCGDerivation(tree)


# test_ccg("create not even list from 0 to 100 that is bigger than 5")
