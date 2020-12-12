from typing import Dict, List

from .visitor import Visitor


class Node:

    def walk(self, v: Visitor):
        pass


class ValueNode(Node):

    def __init__(self, value):
        self.value = value

    def walk(self, v: Visitor):
        if not v.enter_node(self):
            return
        v.leave_node(self)


class NumberNode(ValueNode):

    def __init__(self, value):
        super().__init__(value)


class StringNode(ValueNode):

    def __init__(self, value):
        super().__init__(value)


class TagNode(Node):

    def __init__(
        self,
        name: str = None,
        attrs: Dict[str, Node] = None,
        childrens: List[Node] = None
    ):
        self.name = name
        self.attrs = attrs
        self.childrens = childrens

    def walk(self, v: Visitor):
        if not v.enter_node(self):
            return

        for children in self.childrens:
            children.walk(v)

        v.leave_node(self)
