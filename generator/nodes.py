from abc import ABC, abstractmethod


class Node(ABC):

    def __init__(self):
        self.children = []

    @abstractmethod
    def content_to_string(self) -> str:
        pass


class Test(Node):

    def __init__(self, number: int):
        super().__init__()
        self.number = number

    def content_to_string(self) -> str:
        f"Test [{self.number}]"


class Blank(Node):
    def content_to_string(self) -> str:
        return "Blank"
