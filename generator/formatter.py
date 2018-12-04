from nltk import word_tokenize


def _format_word(word, words):
    if word.isdigit():
        return '~INT~'
    if word in words:
        return word
    return '~UNK~'


def format_sentence(sentence, words, keep_unknown=False):
    """Given sentence and collection of allowed words,
    tokenize and format the sentence"""
    tokens = word_tokenize(sentence.lower(), language='english', preserve_line=False)
    tokens = [_format_word(w, words) for w in tokens]
    if keep_unknown:
        return tokens
    else:
        return [w for w in tokens if w != '~UNK~']
