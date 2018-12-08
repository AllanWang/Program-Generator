import unittest

from generator.ccg import parse

valid_sentences = [
    "create list from 0 to 100",
    "create a list from 0 to 100",
    "create a list to 1 from 99",
    "create even list from 0 to 100",
    "create even list from 0 to 100 that is even",
    "create even list from 0 to 100 that is bigger than 5",
    "create even list from 0 to 100 that is larger than 5",
]

invalid_sentences = [
    "list",
    "create list",
    "create bigger than 5 list from 0 to 100",
    "create donut",
]


class TestCCG(unittest.TestCase):

    def test_valid_sentences(self):
        for sentence in valid_sentences:
            with self.subTest(sentence):
                self.assertIsNotNone(parse(sentence), "Failed to parse")

    def test_invalid_sentences(self):
        for sentence in invalid_sentences:
            with self.subTest(sentence):
                self.assertIsNone(parse(sentence, print_warnings=False), "Parsed invalid program")


if __name__ == '__main__':
    unittest.main()
