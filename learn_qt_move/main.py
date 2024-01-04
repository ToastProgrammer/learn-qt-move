import sys

from dataclasses import dataclass

from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QDial
from PyQt6.QtGui import QPainter

from learn_qt_move.LogTable import XY
from learn_qt_move.LogTable import DataTableWidget
from learn_qt_move.MoveButtons import MoveButtonsWidget


class CharacterGridWindow(QMainWindow):
    grid_size: XY

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Qt Move Application")
        self.buttons = MoveButtonsWidget()
        self.setCentralWidget(self.buttons)
        

    def init_character_grid(self):
        # Clear existing widgets in the grid layout
        # for i in reversed(range(self.grid_layout.count())):
        #     widget = self.grid_layout.itemAt(i).widget()
        #     self.grid_layout.removeWidget(widget)
        #     widget.setParent(None)

        # Add character to the grid layout
        for i in range():
            for j in range(5):
                btn = QPushButton(" ")
                btn.setFixedSize(40, 40)
                self.grid_layout.addWidget(btn, i, j)

        # Update the character position
        # self.update_character_position()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = CharacterGridWindow()
    window.show()

    app.exec()
