from generator.ccg import parse
import unittest
from nltk.ccg import chart

sentences = [
    "create list from 0 to 0",
    "create to 0"
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
