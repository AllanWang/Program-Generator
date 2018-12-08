from nltk import word_tokenize
from typing import List, Iterable, Union, Tuple, Dict, Optional
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import nltk
from enum import unique, IntEnum, auto


@unique
class Status(IntEnum):
    unknown = auto()
    ok = auto()
    ignore = auto()


lemmatizer = WordNetLemmatizer()

tag_to_wordnet = {
    'ADJ': wn.ADJ,
    'ADV': wn.ADV,
    'NOUN': wn.NOUN,
    'VERB': wn.VERB
}


def lemmatize(word: str, tag: str) -> str:
    """
    Given sentence as a list of words,
    output a new list with the lemmas
    """
    wn_tag = tag_to_wordnet.get(tag)
    if wn_tag is None:
        return word
    else:
        return lemmatizer.lemmatize(word, wn_tag)


class Formatter:
    def __init__(self, words: Iterable[str], synset_names: Dict[str, Union[str, List[str]]]):
        """Create and verify the formatter arguments.
        For the formatter, we must supply a list of all valid words.
        We may also add a dictionary mapping words to synset names.
        This will add an additional set of valid tokens, which will be converted into one of the provided words"""
        self._words = words
        if not set(synset_names.keys()).issubset(set(words)):
            raise ValueError("Synset data not a subset of word list")
        synonyms = {}

        def add_synonyms(word, synset_name: str):
            synset = wn.synset(synset_name)
            for synonym in synset.lemma_names():
                if synonym == word:
                    continue
                if synonym in synonyms and synonyms[synonym] != word:
                    raise ValueError(f"Duplicate entry for {synonym}; matches both {word} and {synonyms[synonym]}")
                synonyms[synonym] = word

        for word, s_names in synset_names.items():
            if isinstance(s_names, str):
                add_synonyms(word, s_names)
            else:
                for s in s_names:
                    add_synonyms(word, s)
        self._synonyms = synonyms

    def format_sentence(self, sentence: str) -> Union[Tuple[List[str], Iterable[int]], str]:
        """Given sentence and collection of allowed words,
        tokenize and format the sentence.
        Formatting will satisfy the following:
        - words and their lemmas matching the provided words and numbers are kept as is
        - words and their lemmas matching a synonym will be converted to the associated word
        - unknown words that can be ignored will be ignored. Otherwise an exception is thrown"""
        tokens = word_tokenize(sentence.lower(), language='english', preserve_line=False)
        tagged = nltk.pos_tag(tokens, tagset='universal')
        formatted_tokens: [str] = []
        for word, tag in tagged:
            formatted_word, status = self._get_word_status(word, tag)
            if status == Status.unknown:
                return f"Unknown word '{word}'; cannot be ignored as it has tag '{tag}'"
            if status == Status.ok:
                formatted_tokens.append(formatted_word)
        numbers = (t for t in formatted_tokens if t.isdigit())
        return formatted_tokens, numbers

    def _can_ignore(self, word: str, tag: str) -> bool:
        return tag != 'ADJ' and tag != 'ADV' and tag != 'NOUN'

    def _get_word_status(self, word: str, tag: str) -> (str, Status):
        if word in self._words or word.isdigit():
            return word, Status.ok
        if word in self._synonyms:
            return self._synonyms[word], Status.ok
        lemma = lemmatize(word, tag)
        if lemma in self._words:
            return lemma, Status.ok
        if lemma in self._synonyms:
            return self._synonyms[lemma], Status.ok
        if self._can_ignore(word, tag):
            return word, Status.ignore
        return word, Status.unknown


def test_tags(sentence):
    tagged = nltk.pos_tag(word_tokenize(sentence.lower()))
    print(tagged)


def test_synonyms(*word: str) -> [str]:
    for w in word:
        for s in wn.synsets(w):
            print(s.name(), s.lemma_names(), s.definition())


# test("Create a list from 1 to 100 that is not even")

# test_synonyms('bigger')
