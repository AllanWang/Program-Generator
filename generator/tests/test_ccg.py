from generator.ccg import parse
import unittest
from nltk.ccg import chart

valid_sentences = [
    "create list from 0 to 100",
    "create even list from 0 to 100",
    "create even list from 0 to 100 that is even",
    "create even list from 0 to 100 that is bigger than 5"
]

invalid_sentences = [
    "create list",
    "create bigger than 5 list from 0 to 100"
]


class TestGenerator(unittest.TestCase):

    def test_valid_sentences(self):
        for sentence in valid_sentences:
            with self.subTest(sentence):
                self.assertIsNotNone(parse(sentence), "Failed to parse")

    def test_invalid_sentences(self):
        for sentence in invalid_sentences:
            with self.subTest(sentence):
                self.assertIsNone(parse(sentence), "Parsed invalid program")


if __name__ == '__main__':
    unittest.main()
