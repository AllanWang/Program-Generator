from .nodes import Node


class Result:
    def __init__(self, request: str, formatted_request: str, tree: Node):
        self.input = request
        self.formatted_input = formatted_request
        self.tree = tree

    def __repr__(self):
        return "result"
