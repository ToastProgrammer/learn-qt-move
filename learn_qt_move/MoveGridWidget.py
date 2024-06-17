import logging
from MoveButtons import MoveButtonsWidget
from PlayerGridWidget import PlayerGridWidget

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import pyqtSlot


class MoveGridWidget(QWidget):
    m_buttons: MoveButtonsWidget
    m_grid: PlayerGridWidget
    logger: logging.Logger
    
    def __init__(self, log_level: int = logging.ERROR):
        super().__init__()
        
        # Child Widgets
        self.m_buttons = MoveButtonsWidget()
        self.m_grid = PlayerGridWidget()
        
        # Signals
        self.m_buttons.button_press.connect(self.handle_button_press)
        self.m_grid.debug_msg_signal.connect(self.debug_msg)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.m_grid)
        layout.addWidget(self.m_buttons)
        self.setLayout(layout)
        self.setup_logging(log_level)

    def setup_logging(self, log_level: int):
        self.logger = logging.getLogger(__name__)
        _handler = logging.StreamHandler()
        _formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        _handler.setFormatter(_formatter)
        self.logger.addHandler(_handler)
        self.logger.setLevel(log_level)
        
    @pyqtSlot(str)
    def handle_button_press(self, direction: str):
        self.m_grid.move_player_by_space(direction)
        
    @pyqtSlot(str)
    def debug_msg(self, message: str):
        self.logger.debug(message)

if __name__ == "__main__":
    app = QApplication([])
    window = MoveGridWidget(logging.DEBUG)
    window.show()
    app.exec()
