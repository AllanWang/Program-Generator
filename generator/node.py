from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Node:
    value: str
    children: List['Node']
    parent: Optional['Node']

    def add_child(self, value) -> 'Node':
        child = Node(value, [], self)
        self.children.append(child)
        return child

    @classmethod
    def parse(cls, tree: str, down_char: chr = '(', up_char: chr = ')', sep_char: chr = ',',
              ignore_whitespace: bool = True) -> Optional['Node']:
        node = Node(value='', children=[], parent=None)
        value: [chr] = []

        def update_value():
            nonlocal node
            nonlocal value
            if value:
                node.value = ''.join(value)
            value.clear()

        for c in tree:
            if c == down_char:
                update_value()
                node = node.add_child('')
            elif c == sep_char:
                update_value()
                node = node.parent.add_child('')
            elif c == up_char:
                update_value()
                node = node.parent
            else:
                if not ignore_whitespace or not c.isspace():
                    value.append(c)

        update_value()

        if node.parent is not None:
            # bracket mismatch
            return None
        return node

    def display(self, down_char: chr = '(', up_char: chr = ')', sep_char: chr = ',') -> str:
        children_display = [c.display(down_char, up_char, sep_char) for c in self.children]
        if children_display:
            return f"{self.value}{down_char}{sep_char.join(children_display)}{up_char}"
        return f"{self.value}"
