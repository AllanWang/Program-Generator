from typing import Optional
from generator.result import Result
from generator.condition import Condition
from nltk import word_tokenize, pos_tag, BottomUpChartParser, Production
import nltk
from beeprint import pp
from pprint import pprint

grammar: nltk.CFG = nltk.data.load('file:../static/grammar.cfg')
terminals: [str] = filter(nltk.grammar.is_terminal,
                          [r for rhs in map(Production.rhs, grammar.productions()) for r in rhs])


def is_key(word: str) -> bool:
    return word.startswith('#') and word.endswith('#')


def splitter(pred, data):
    yes, no = [], []
    for d in data:
        (yes if pred(d) else no).append(d)
    return [yes, no]


(terminal_keys, terminal_words) = splitter(is_key, terminals)

print(f"Terminal keys: {terminal_keys}")
print(f"Terminal words: {terminal_words}")


def generate(query: str) -> Result:
    tokens = word_tokenize(query.lower(), language='english', preserve_line=False)
    tagged_query = pos_tag(tokens, tagset='universal')

    formatted_tokens = []
    for token in tagged_query:
        (word, tag) = token
        result = format(token)
        if result is not None:
            formatted_tokens.append((result, tag))
    conditions = []

    for index, word in enumerate(formatted_tokens):
        condition, parsed = get_condition(word, index, formatted_tokens)
        if not parsed:
            return Result(tokens=tokens, formatted_tokens=formatted_tokens, fully_parsed=False,
                          conditions=conditions)
        if condition is not None:
            conditions.append(condition)
    return Result(tokens=tokens, formatted_tokens=formatted_tokens, fully_parsed=True, conditions=conditions)


def format(token: (str, str)) -> Optional[str]:
    (word, tag) = token
    """Given input token,
    either format the token or remove it"""
    if word.isdigit():
        return '~INT~'
    if word == 'bigger':
        return '~BT~'
    return word if word in terminal_words else None


"""
Universal Tagset

ADJ	adjective	new, good, high, special, big, local
ADP	adposition	on, of, at, with, by, into, under
ADV	adverb	really, already, still, early, now
CONJ	conjunction	and, or, but, if, while, although
DET	determiner, article	the, a, some, most, every, no, which
NOUN	noun	year, home, costs, time, Africa
NUM	numeral	twenty-four, fourth, 1991, 14:24
PRT	particle	at, on, out, over per, that, up, with
PRON	pronoun	he, their, her, its, my, I, us
VERB	verb	is, say, told, given, playing, would
.	punctuation marks	. , ; !
X	other	ersatz, esprit, dunno, gr8, univeristy
"""

ignored_tags = ['CONJ', 'DET', 'PRT', '.', 'X']


def get_condition(tagged_key: (str, str), index: int, tagged_phrase: [(str, str)]) -> (Optional[Condition], bool):
    word, tag = tagged_key
    if tag in ignored_tags:
        return None, True
    return None, False


if __name__ == '__main__':
    grammar: nltk.CFG = nltk.data.load('file:../static/grammar.cfg')
    terminals = filter(nltk.grammar.is_terminal, [r for rhs in map(Production.rhs, grammar.productions()) for r in rhs])

    parser = BottomUpChartParser(grammar)
    result = generate("Create list from 0 to 1")
    pp(result)
    tokens = [token[0] for token in result.formatted_tokens]
    print(tokens)
    parser.parse(tokens).pretty_print()
