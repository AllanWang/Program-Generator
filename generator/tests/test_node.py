import unittest

from generator.node import Node

valid_trees = [
    "a",
    "a(b)",
    "a(b(c))",
    "ab(cd)",
    "ab(cd, ef(g(c, d)))"
]


class TestNode(unittest.TestCase):

    def test_valid_nodes(self):
        for tree in valid_trees:
            with self.subTest(tree):
                self.assertEqual(tree, Node.parse(tree).display(), 'Parse mismatch')


if __name__ == '__main__':
    unittest.main()
