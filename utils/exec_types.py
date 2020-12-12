from PyQt5 import QtCore


class Value:

    def __init__(self, value=None):
        self.value = value

    def exec(self):
        pass


class String(Value):

    def __init__(self, value):
        super().__init__(value)

    def exec(self) -> str:
        return self.value


class Number(Value):

    def __init__(self, value):
        super().__init__(value)

    def exec(self):
        return self.value


class Rect(Value):

    def __init__(self, value):
        super().__init__(value)

    def exec(self) -> QtCore.QRect:
        x, y, w, h = self.value
        return QtCore.QRect(x, y, w, h)


class Size(Value):

    def __init__(self, value):
        super().__init__(value)

    def exec(self) -> QtCore.QSize:
        x, y = self.value
        return QtCore.QSize(x, y)