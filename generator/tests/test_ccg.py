from generator.ccg import parse
import unittest
from nltk.ccg import chart

sentences = [
    # "from 0 to 0 create list",
    # "create even list from 0 to 0",
    # "create list from 0 to 0 if bigger 5",
    # "create even list from 0 to 0 and if bigger 5"
    "the dog bit john",
    "the dog john bit"
]


class TestGenerator(unittest.TestCase):

    def test(self):
        for sentence in sentences:
            with self.subTest():
                for result in parse(sentence):
                    chart.printCCGDerivation(result)
                    break


if __name__ == '__main__':
    unittest.main()
