"""
"""
from dataclasses import dataclass
from functools import cache
from typing import Optional

from PyQt6.QtCore import QLine, QPoint, QRect, QSize, Qt
from PyQt6.QtGui import QBrush, QPainter, QPaintEvent, QPen
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QVBoxLayout


from common import BRUSH_BLUE_SOLID, PEN_BLACK_MEDIUM


DEFAULT_GRID_AREA = QRect(20, 20, 300, 300)
DEFAULT_TOTAL_SIZE = QSize(340, 380)
DEFAULT_GRID_CELLS = QSize(5,5)

class PlayerGridWidget(QWidget):
    """
    """
    
    # total_size: QSize  # Size of the widget; grid + borders
    num_cells: QSize    # Number of discrete spaces in the grid
    
    grid_area: QRect    # Size of area where the grid is drawn
    
    def __init__(
        self,
        num_cells: QSize = DEFAULT_GRID_CELLS,
        grid_area: Optional[QRect] = DEFAULT_GRID_AREA
        ):
        super().__init__()
        
        self.setGeometry(grid_area)
        self.grid_area = grid_area
        
        self.num_cells = num_cells 
        
        self.update()   # Trigger repaint


    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(QPen(*PEN_BLACK_MEDIUM))
        painter.setBrush(QBrush(*BRUSH_BLUE_SOLID))
        
        # Set coordinates relative to grid area instead of the widget
        painter.translate(self.grid_area.topLeft())     
        
        # Draw Background
        painter.drawRect(self.grid_area)
        
        # Draw Vertical lines for columns
        for h in range(1,self.num_cells.width()):
            pos = self.grid_area.width() // self.num_cells.width() * h + self.grid_area.left()
            painter.drawLine(
                QPoint(pos, self.grid_area.top()),      # (x,y)
                QPoint(pos, self.grid_area.bottom())    # (dx,dy)
                )
            
        # Draw Horizontal lines for Rows
        for v in range(1,self.num_cells.height()):
            pos = self.grid_area.height() // self.num_cells.height() * v + self.grid_area.top()
            painter.drawLine(
                QPoint(self.grid_area.left(), pos), 
                QPoint(self.grid_area.right(), pos)
                )
            
    
def size_fits_in_rect(size: QSize, rect: QRect):
    return size.width() <= rect.width() and size.height() <= rect.height()
            

if __name__ == "__main__":
    app = QApplication([])
    window = PlayerGridWidget()
    window.show()
    app.exec()
