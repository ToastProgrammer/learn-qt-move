from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal

class MoveButtonsWidget(QWidget):
    """

    """

    button_press = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        _up = QPushButton("^")
        _down = QPushButton("v")
        _left = QPushButton("<")
        _right = QPushButton(">")

        # Need to connect lambda to pass pyqtSignal as argument, otherwise passes `None`
        _up.clicked.connect(lambda: self.button_press.emit("up"))
        _down.clicked.connect(lambda: self.button_press.emit("down"))
        _left.clicked.connect(lambda: self.button_press.emit("left"))
        _right.clicked.connect(lambda: self.button_press.emit("right"))

        self.layout = QGridLayout()
        self.layout.addWidget(_up, 0, 1)
        self.layout.addWidget(_down, 2, 1)
        self.layout.addWidget(_left, 1, 0)
        self.layout.addWidget(_right, 1, 2)

        self.setLayout(self.layout)
