from MoveButtons import MoveButtonsWidget
from PyQt6.QtWidgets import QWidget


class MoveGridWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.m_buttons = MoveButtonsWidget()

        # TODO: Add GridManagerWidget
        # TODO: Add EventLogWidget
