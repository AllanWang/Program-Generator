import unittest

from generator.code_gen_templates import *

sentences: [(str, [int])] = [
    ("create list from 0 to 100",
     [x for x in range(0, 101)]),
    ("create a list from 0 to 100",
     [x for x in range(0, 101)]),
    ("create a list to 1 from 99",
     [x for x in reversed(range(1, 100))]),
    ("create even list from 0 to 100",
     [x for x in range(0, 101) if x % 2 == 0]),
    ("create even list from 0 to 100 that is even",
     [x for x in range(0, 101) if x % 2 == 0]),
    ("create even list from 0 to 100 that is bigger than 5",
     [x for x in range(0, 101) if x % 2 == 0 and x > 5]),
    ("create even list from 0 to 100 that is not even",
     []),
    ("create even list from 0 to 100 that is not not odd",
     [])
]


class TestCodeGen(unittest.TestCase):

    def _get_output(self, language_name: str, code: str) -> [int]:
        if language_name.startswith('python'):
            output = {}
            exec(f"{code}\n\nresult = code()", globals(), output)
            self.assertIsInstance(output['result'], list, "Could not get list output from python code")
            return output['result']
        return []

    def _test_sentence(self, language: CodeGenLanguage, verify_output: bool = True):
        for (sentence, expected) in sentences:
            with self.subTest(sentence):
                node = parse_to_node(sentence)
                code = language.generate_from_node(node)
                if not node:
                    self.fail("Could not create node from sentence")
                if verify_output:
                    try:
                        result = self._get_output(language.name, code)
                        self.assertEqual(expected, result, "Output mismatch")
                    except:
                        self.fail(f"Bad output\n{code}")
                else:
                    print(f"-----\n{sentence}\n{code}\n-----")

    def test_python_inline(self):
        self._test_sentence(CodeGenLanguage.from_templates('python_inline', code_gen_python_inline_templates))

    def test_python_functional(self):
        self._test_sentence(CodeGenLanguage.from_templates('python_functional', code_gen_python_functional_templates))

    def test_java(self):
        self._test_sentence(CodeGenLanguage.from_templates('java', code_gen_java_templates), False)

    def test_kotlin(self):
        self._test_sentence(CodeGenLanguage.from_templates('kotlin', code_gen_kotlin_templates), False)

    def test_elm(self):
        self._test_sentence(CodeGenLanguage.from_templates('elm', code_gen_elm_templates), False)


if __name__ == '__main__':
    unittest.main()
