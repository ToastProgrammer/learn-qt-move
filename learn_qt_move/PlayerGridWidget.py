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
from common import DEFAULT_GRID_SIZE, DEFAULT_CANVAS_RECT


class PlayerGridWidget(QWidget):
    """
    """
    
    canvas_size: QRect
    grid_size: QRect
    num_cells: QSize
    
    def __init__(self, num_cells: QSize = QSize(5,5), canvas_size: Optional[QSize] = None, grid_size: Optional[QSize] = None):
        super().__init__()
        
        try:
            self.resize(*canvas_size)
            self.canvas_size = canvas_size
        except(TypeError):
            self.resize(DEFAULT_GRID_SIZE)
            self.canvas_size = DEFAULT_CANVAS_RECT
        
        self.grid_size = grid_size if grid_size and grid_size < self.canvas_size else self.canvas_size
        self.num_cells = num_cells 
        
        self.update()


    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(QPen(*PEN_BLACK_MEDIUM))
        painter.setBrush(QBrush(*BRUSH_BLUE_SOLID))
        
        # Draw Background
        painter.drawRect(self.canvas_size)
        
        # Draw Column lines
        for h in range(1,self.num_cells.width()):
            pos = self.grid_size.width() // self.num_cells.width() * h
            painter.drawLines(
                QPoint(pos, self.grid_size.top()), 
                QPoint(pos, self.grid_size.bottom())
                )
            
            
        # Draw Row lines
        for v in range(1,self.num_cells.height()):
            pos = self.grid_size.height() // self.num_cells.height() * v
            painter.drawLines(
                QPoint(self.grid_size.left(), pos), 
                QPoint(self.grid_size.right(), pos)
                )
            

if __name__ == "__main__":
    app = QApplication([])
    window = PlayerGridWidget()
    window.show()
    app.exec()
