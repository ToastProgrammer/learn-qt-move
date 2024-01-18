"""
"""
from dataclasses import dataclass
from contextlib import contextmanager
from functools import cache
from typing import Optional
from typing import List
from typing import Tuple

from PyQt6.QtCore import QLine, QPoint, QRect, QSize, Qt, QMargins
from PyQt6.QtGui import QBrush, QPainter, QPaintEvent, QPen
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QVBoxLayout


from common import XY
from common import BRUSH_BLU_SLD, PEN_BLA_MED, PEN_GRY_SML
from PainterUtils import draw_grid


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
        
        self.setGeometry(grid_area.marginsAdded(QMargins(30,10,30,60)))
        self.grid_area = grid_area
        self.num_cells = num_cells 
        
        self.update()   # Trigger repaint


    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        
        # TODO: Move save/restore to context manager
        painter.save()
        
        # Set coordinates relative to grid area instead of the widget
        painter.translate(self.grid_area.topLeft())
        
        draw_grid(painter, self.grid_area, self.num_cells, PEN_BLA_MED, brush_style=BRUSH_BLU_SLD)
        draw_grid(painter, self.grid_area, self.num_cells, PEN_GRY_SML, offset=XY(2,2))
        
        painter.restore()
            
    
def size_fits_in_rect(size: QSize, rect: QRect):
    return size.width() <= rect.width() and size.height() <= rect.height()
            

if __name__ == "__main__":
    app = QApplication([])
    window = PlayerGridWidget()
    window.show()
    app.exec()
