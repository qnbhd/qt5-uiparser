from PyQt5.QtWidgets import *
from utils.treemaker import TreeMaker
from runners.printer import Printer
from runners.executor import Executor

import sys
from PyQt5 import QtWidgets


class ExampleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        with open("mainwindow.ui") as source:
            text = source.read()
            tm = TreeMaker(text)
            ast = tm.make()
            printer = Printer()
            executor = Executor(self)
            ast.walk(printer)
            ast.walk(executor)


def main():
    app = QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
