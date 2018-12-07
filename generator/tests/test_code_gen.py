import unittest

from generator.ccg import parse_to_node
from generator.code_gen import *

sentences: [(str, [int])] = [
    ("create list from 0 to 100",
     [x for x in range(0, 100)]),
    ("create a list from 0 to 100",
     [x for x in range(0, 100)]),
    ("create a list to 1 from 99",
     [x for x in reversed(range(1, 99))]),
    ("create even list from 0 to 100",
     [x for x in range(0, 100) if x % 2 == 0]),
    ("create even list from 0 to 100 that is even",
     [x for x in range(0, 100) if x % 2 == 0]),
    ("create even list from 0 to 100 that is bigger than 5",
     [x for x in range(0, 100) if x % 2 == 0 and x > 5])
]


class TestCodeGen(unittest.TestCase):

    def _get_output(self, language_name: str, code: str) -> [int]:
        if language_name.startswith('python'):
            output = {}
            exec(f"{code}\n\nresult = code()", globals(), output)
            self.assertIsInstance(output['result'], list, "Could not get list output from python code")
            return output['result']
        return []

    def _test_sentence(self, language: CodeGenLanguage):
        for (sentence, expected) in sentences:
            with self.subTest(sentence):
                node = parse_to_node(sentence)
                if not node:
                    self.fail("Could not create node from sentence")
                result = self._get_output(language.name, language.generate_from_node(node))
                self.assertEqual(expected, result, "Output mismatch")

    def test_python_inline(self):
        self._test_sentence(code_gen_python_inline)

    def test_python_functional(self):
        self._test_sentence(code_gen_python_functional)


if __name__ == '__main__':
    unittest.main()
