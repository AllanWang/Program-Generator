import unittest

from generator.node import Node

valid_trees = [
    "a",
    "a(b)",
    "a(b(c))",
    "ab(cd)",
    "ab(cd, ef(g(c, d)))"
]

invalid_trees = [
    "(a)",
    "a(b",
    "a(b))",
    "a(b)(c)"
]


class TestNode(unittest.TestCase):

    def test_valid_nodes(self):
        for tree in valid_trees:
            with self.subTest(tree):
                tree = "".join(tree.split())  # Remove whitespace
                self.assertEqual(tree, Node.parse(tree).display(), 'Parse mismatch')

    def test_invalid_nodes(self):
        for tree in invalid_trees:
            with self.subTest(tree):
                tree = "".join(tree.split())  # Remove whitespace
                self.assertIsNone(Node.parse(tree), "Parsed invalid tree")


if __name__ == '__main__':
    unittest.main()
