from nltk import word_tokenize
from typing import List


def _format_word(word, words):
    if word in words or word.isdigit():
        return word
    return '~UNK~'


def format_sentence(sentence, words, keep_unknown=False) -> (List[str], List[int]):
    """Given sentence and collection of allowed words,
    tokenize and format the sentence"""
    tokens = word_tokenize(sentence.lower(), language='english', preserve_line=False)
    tokens = [_format_word(w, words) for w in tokens]
    numbers = [t for t in tokens if t.isdigit()]
    if keep_unknown:
        return tokens, numbers
    else:
        return [w for w in tokens if w != '~UNK~'], numbers
