from utils.astnodes import *


class Printer(Visitor):

    def __init__(self):
        self.indent = 0

    def print_indent(self, relative):
        for i in range(0, self.indent + relative):
            print("  ", end='')

    def print(self, *args, **kwargs):
        self.print_indent(0)
        print("+-", *args, **kwargs)

    def enter_node(self, node) -> bool:

        if isinstance(node, TagNode):
            self.print(f"Tag [{node.name}]")
            self.indent += 1
            self.print("Attributes: ")
            self.indent += 1
            for attr, value in node.attrs.items():
                self.print(f"Attr [{attr}]:")
                self.indent += 1
                value.walk(self)
                self.indent -= 1
            self.indent -= 1
            for children in node.childrens:
                children.walk(self)
            return False
        if isinstance(node, ValueNode):
            self.print(f"Value Node: [{node.value}]")
            return False
        if isinstance(node, NumberNode):
            self.print(f"Number Node: [{node.value}]")
            return False
        if isinstance(node, StringNode):
            self.print(f"String Node: [{node.value}]")
            return False

        return True

    def leave_node(self, node):
        self.indent -= 1
