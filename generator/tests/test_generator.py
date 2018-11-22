import unittest
from generator.generate import generate

generator_values = [
    ("this is a test", [])
]

failed_generator_values = [
    "this is a test"
]


class TestGenerator(unittest.TestCase):

    def test_valid_generators(self):
        for query, expected in generator_values:
            with self.subTest():
                result = generate(query)
                self.assertTrue(result.fully_parsed)
                self.assertEqual(result.conditions, expected)

    def test_invalid_generators(self):
        for query in failed_generator_values:
            with self.subTest():
                result = generate(query)
                self.assertFalse(result.fully_parsed)


if __name__ == '__main__':
    unittest.main()
