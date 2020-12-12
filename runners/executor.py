from typing import Callable

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from utils.astnodes import *
from utils.exec_types import *


def ClassFactory(classname, *args, **kwargs):
    cls = globals()[classname]
    return cls(*args, **kwargs)


# noinspection PyPropertyAccess
class Executor(Visitor):

    def __init__(self, main_window: QtWidgets.QMainWindow):
        self.main_window = main_window
        self._last_value: Value = Value()
        self.current_object = main_window

    last_value = property()

    @last_value.getter
    def last_value(self):
        return self._last_value.exec()

    @last_value.setter
    def last_value(self, value):
        self._last_value = value

    def _rect(self, node):
        assert len(node.childrens) == 4, "invalid rect"
        node.childrens[0].walk(self)
        x = self.last_value
        node.childrens[1].walk(self)
        y = self.last_value
        node.childrens[2].walk(self)
        w = self.last_value
        node.childrens[3].walk(self)
        h = self.last_value
        self.last_value = Rect((x, y, w, h))

    def _string(self, node):
        assert len(node.childrens) == 1, "invalid string"
        node.childrens[0].walk(self)

    def _param(self, node):
        assert len(node.childrens) == 1, "invalid param"
        node.childrens[0].walk(self)

    def _ui(self, node):
        for children in node.childrens:
            children.walk(self)

    def _size(self, node):
        assert len(node.childrens) == 2, "invalid string"
        node.childrens[0].walk(self)
        x = self.last_value
        node.childrens[1].walk(self)
        y = self.last_value
        self.last_value = Size((x, y))

    def _property(self, node):
        node.attrs["name"].walk(self)
        prop_name = self.last_value
        children = node.childrens[0]
        children.walk(self)
        value = self.last_value
        if prop_name == 'geometry':
            if isinstance(value, QtCore.QRect):
                self.current_object.setGeometry(value)
        elif prop_name == "text":
            if isinstance(value, str):
                self.current_object.setText(value)

    def _widget(self, node):
        node.attrs["class"].walk(self)
        # for type check
        class_ = str(self.last_value)
        node.attrs["name"].walk(self)
        name = str(self.last_value)
        if name == 'MainWindow':
            self.current_object = self.main_window
            prev_parent = self.main_window
        else:
            instance: QWidget = ClassFactory(
                f"{class_}", self.current_object
            )
            prev_parent = self.current_object
            self.current_object = instance

        self.current_object.setObjectName(name)

        # special
        if name == "centralwidget":
            self.main_window.setCentralWidget(self.current_object)
        if class_ == "QMenuBar":
            if isinstance(self.current_object, QMenuBar):
                self.main_window.setMenuBar(self.current_object)
        if class_ == "QStatusBar":
            if isinstance(self.current_object, QStatusBar):
                self.main_window.setStatusBar(self.current_object)

        for children in node.childrens:
            children.walk(self)
        self.current_object = prev_parent

    def enter_node(self, node) -> bool:

        if isinstance(node, TagNode):
            tag_name = node.name
            handlers: Dict[str, Callable] = dict(
                ui=self._ui,
                x=self._param,
                y=self._param,
                width=self._param,
                height=self._param,
                string=self._string,
                rect=self._rect,
                size=self._size,
                property=self._property,
                widget=self._widget
            )
            handler = handlers.get(tag_name, None)
            if handler:
                handler(node)
            return False
        # not change order!
        if isinstance(node, NumberNode):
            self.last_value = Number(node.value)
            return False
        if isinstance(node, StringNode):
            self.last_value = String(node.value)
            return False
        if isinstance(node, ValueNode):
            self.last_value = String(node.value)
            return False
        return True

    def leave_node(self, node):
        pass
