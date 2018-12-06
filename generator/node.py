from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Node:
    value: str
    children: List['Node']

    def add_child(self, value) -> 'Node':
        child = Node(value, [])
        self.children.append(child)
        return child

    @classmethod
    def parse(cls, tree: str, down_char: chr = '(', up_char: chr = ')', sep_char: chr = ',',
              ignore_whitespace: bool = True, allow_blank_values: bool = False) -> Optional['Node']:
        """
        Parses the provided string into a node tree.
        :param tree: parse input
        :param down_char: character indicating we are going down a level
        :param up_char: character indicating we are going up a level
        :param sep_char: character separating nodes of the same level
        :param ignore_whitespace: true to ignore any whitespace characters
        :param allow_blank_values: true to allow nodes with empty string as value
        :return: root node if parsed properly, none otherwise.
        """
        if tree.count(down_char) != tree.count(up_char):
            return None
        node: Node = Node(value='', children=[])
        parent_stack: [Node] = []
        value: [chr] = []

        def update_value(require_value: bool) -> bool:
            """
            Updates the value of the current node
            :return: true if parsing should continue; false if an error occurred
            """
            nonlocal node
            nonlocal value

            if value:
                if node.value is not '':
                    return False
                node.value = ''.join(value)
                value.clear()
                return True
            return not require_value and (allow_blank_values or node.value is not '')

        for c in tree:
            if c == down_char:
                if not update_value(True):
                    return None
                parent_stack.append(node)
                node = node.add_child('')
            elif c == sep_char:
                if not update_value(True):
                    return None
                if not parent_stack:
                    return None
                node = parent_stack[-1].add_child('')
            elif c == up_char:
                if not update_value(False):
                    return None
                if not parent_stack:
                    return None
                else:
                    node = parent_stack[-1]
                    del parent_stack[-1]
            else:
                if not ignore_whitespace or not c.isspace():
                    value.append(c)

        if not update_value(False):
            return None

        if parent_stack:
            # bracket mismatch; not at root
            return None
        return node

    def display(self, down_char: chr = '(', up_char: chr = ')', sep_char: chr = ',') -> str:
        """
        Returns a human readable string with the current node as root
        :param down_char: character indicating we are going down a level
        :param up_char: character indicating we are going up a level
        :param sep_char: character separating nodes of the same level
        :return:
        """
        children_display = [c.display(down_char, up_char, sep_char) for c in self.children]
        if children_display:
            return f"{self.value}{down_char}{sep_char.join(children_display)}{up_char}"
        return f"{self.value}"
