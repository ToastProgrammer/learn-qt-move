import sys

from dataclasses import dataclass

from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QDial
from PyQt6.QtGui import QPainter

from learn_qt_move.LogTable import XY
from learn_qt_move.MoveGridWidget import MoveGridWidget
from learn_qt_move.MoveButtons import MoveButtonsWidget


class CharacterGridWindow(QMainWindow):
    grid_size: XY

    def __init__(self):
        super().__init__()

        # Initial Window properties
        self.setWindowTitle("Qt Move Application")
        self.resize(400, 400)

        # Initialize main widget
        self.grid_widget = MoveGridWidget()

        # Define Layout
        layout = QVBoxLayout()
        layout.addWidget(self.grid_widget)

        self._finalize_layout(layout)


    def _finalize_layout(self, layout) -> None:
        """
        """
        container  = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = CharacterGridWindow()
    window.show()

    app.exec()
