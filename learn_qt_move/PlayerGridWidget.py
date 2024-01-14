"""
"""
from dataclasses import dataclass
from functools import cache
from typing import Optional

from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QPen
from PyQt6.QtGui import QBrush
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QRect
from PyQt6.QtCore import QLine
from PyQt6.QtCore import QPoint
from PyQt6.QtCore import QSize


from common import PEN_BLACK_MEDIUM
from common import BRUSH_BLUE_SOLID


DEFAULT_GRID_SIZE_RECT = QRect(20, 20, 300, 300)
DEFAULT_GRID_WIDGET_SIZE = QSize(340, 380)


class PlayerGridWidget(QWidget):
    """
    """
    
    widget_size: QRect  # Size of the widget; grid + borders
    grid_area: QRect    # Area where the grid is drawn
    
    num_cells: QSize    # Number of discrete spaces in the grid
    
    def __init__(self, num_cells: QSize = QSize(5,5), widget_size: Optional[QSize] = None, grid_size: Optional[QSize] = None):
        super().__init__()
        
        try:
            self.resize(*widget_size)
            self.widget_size = widget_size
        except(TypeError):
            self.resize(DEFAULT_GRID_WIDGET_SIZE)
            self.widget_size = DEFAULT_GRID_SIZE_RECT
        
        self.grid_area = grid_size if grid_size and grid_size < self.widget_size else self.widget_size
        self.num_cells = num_cells 
        
        self.update()   # Trigger repaint


    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(QPen(*PEN_BLACK_MEDIUM))
        painter.setBrush(QBrush(*BRUSH_BLUE_SOLID))
        
        # Draw Background
        painter.drawRect(self.widget_size)
        
        # Draw Vertical lines for columns
        for h in range(1,self.num_cells.width()):
            pos = self.grid_area.width() // self.num_cells.width() * h 
            painter.drawLine(
                QPoint(pos, self.grid_area.top()),      # (x,y)
                QPoint(pos, self.grid_area.bottom())    # (dx,dy)
                )
            
        # Draw Horizontal lines for Rows
        for v in range(1,self.num_cells.height()):
            pos = self.grid_area.height() // self.num_cells.height() * v
            painter.drawLine(
                QPoint(self.grid_area.left(), pos), 
                QPoint(self.grid_area.right(), pos)
                )
        
    
            

if __name__ == "__main__":
    app = QApplication([])
    window = PlayerGridWidget()
    window.show()
    app.exec()
