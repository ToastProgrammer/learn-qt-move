"""
"""
from dataclasses import dataclass
from functools import cache
from typing import Optional

from PyQt6.QtCore import QLine, QPoint, QRect, QSize, Qt
from PyQt6.QtGui import QBrush, QPainter, QPaintEvent, QPen
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QVBoxLayout


from common import XY
from common import BRUSH_BLUE_SOLID, PEN_BLACK_MEDIUM


DEFAULT_GRID_AREA = QRect(20, 20, 300, 300)
DEFAULT_TOTAL_SIZE = QSize(340, 380)
DEFAULT_GRID_CELLS = XY(5,5)

class PlayerGridWidget(QWidget):
    """
    """
    num_cells: XY       # Number of discrete spaces in the grid
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
        
        draw_grid(painter, self.grid_area, self.num_cells, PEN_BLACK_MEDIUM, offset=XY(10,10), brush_style=BRUSH_BLUE_SOLID)
        
            
def draw_grid(
    painter: QPainter,
    area: QRect,
    num_cells: XY,
    pen_style: QPen,
    offset: XY = XY(0,0),
    brush_style: Optional[QBrush] = None,
    ) -> None:

    painter.setPen(QPen(*pen_style))
    
    # Set coordinates relative to grid area instead of the widget
    painter.translate(area.topLeft())
    
    # Draw Background
    if brush_style:
        painter.setBrush(QBrush(*brush_style))
        painter.drawRect(area)
    
    # Draw Vertical Lines for Columns
    for h in range(1,num_cells.x):
        pos = area.width() // num_cells.x * h + area.left() + offset.x
        painter.drawLine(
            QPoint(pos, area.top()),    # (x,y)
            QPoint(pos, area.bottom())  # (dx,dy)
            )
            
    # Draw Horizontal lines for Rows
    for v in range(1,num_cells.y):
        pos = area.height() // num_cells.y * v + area.top() + offset.y
        painter.drawLine(
            QPoint(area.left(), pos), 
            QPoint(area.right(), pos)
            )
            
    
def size_fits_in_rect(size: QSize, rect: QRect):
    return size.width() <= rect.width() and size.height() <= rect.height()
            

if __name__ == "__main__":
    app = QApplication([])
    window = PlayerGridWidget()
    window.show()
    app.exec()
