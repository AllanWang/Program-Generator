from abc import ABC, abstractmethod


class Node(ABC):

    def __init__(self):
        self.children = []

    @abstractmethod
    def __repr__(self):
        pass


class Test(Node):

    def __init__(self, number: int):
        super().__init__()
        self.number = number

    def __repr__(self):
        f"Test [{self.number}]"


class IntList(Node):

    def __init__(self, range: (int, int), conditions: []):
        super().__init__()
        self.range = range
        self.conditions = conditions


class Blank(Node):
    def __repr__(self) -> str:
        return "Blank"
