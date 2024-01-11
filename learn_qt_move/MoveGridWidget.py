import sys
from MoveButtons import MoveButtonsWidget


from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout


class MoveGridWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        m_buttons = MoveButtonsWidget()

        # TODO: Add GridManagerWidget
        # TODO: Add EventLogWidget

        layout.addWidget(m_buttons)
        self.setLayout(layout)

    def show_debug(self):
        print("Children:")
        for child in self.children():
            print(f"\t{child}")
