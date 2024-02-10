"""
"""
from dataclasses import dataclass
from contextlib import contextmanager
from functools import cache
from typing import Optional
from typing import List
from typing import Tuple
from typing import Collection

from PyQt6.QtCore import QLine, QPoint, QRect, QRectF, QSize, Qt, QMargins
from PyQt6.QtGui import QBrush, QPainter, QPaintEvent, QPen, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt6.QtWidgets import QVBoxLayout


from common import XY
from common import BRUSH_BLU_SLD, BRUSH_RED_SLD, PEN_BLA_MED, PEN_GRY_SML
from common import GridInvalidError

from PainterUtils import draw_grid


DEFAULT_GRID_AREA = QRect(0, 0, 300, 300)
DEFAULT_TOTAL_SIZE = QSize(340, 340)
DEFAULT_GRID_CELLS = XY(5,5)


class DrawGridWidget(QWidget):
    """
    """
    grid_num_cells: XY       # Number of discrete spaces in the grid
    grid_area: QRect    # Size of area where the grid is drawn
    grid_pixmap: QPixmap
    grid_details: Tuple[XY, Tuple[QPoint, ...]]
    player_index: Optional[XY] = None
    
    
    def __init__(
        self,
        num_cells: XY = DEFAULT_GRID_CELLS,
        grid_area: QRect = DEFAULT_GRID_AREA
        ):
        super().__init__()
        
        # self.setGeometry(grid_area.marginsAdded(QMargins(30,10,30,60)))
        self.grid_area = grid_area
        self.grid_num_cells = num_cells
        self.grid_pixmap = QPixmap(grid_area.width(), grid_area.height())
        
        self.paint_grid()

    def paint_grid(self):
        # Set painter to use the pixmap as a canvas instead of the widget itself
        painter = QPainter(self.grid_pixmap)
        
        # TODO: Move save/restore to context manager
        painter.save()
        try:
            # Set coordinates relative to grid area instead of the widget
            painter.translate(self.grid_area.topLeft())
            
            self.grid_details = draw_grid(painter, self.grid_area, self.grid_num_cells, PEN_BLA_MED, brush_style=BRUSH_BLU_SLD)
            draw_grid(painter, self.grid_area, self.grid_num_cells, PEN_GRY_SML, offset=XY(2,2))
            
        finally:
            painter.restore()
        painter.end()
            
        if not self.grid_details:
            raise GridInvalidError("An error occured when trying to draw the grid, as no space indices were defined.")
        
    def get_pixmap(self):
        return self.grid_pixmap

class DrawPlayerWidget(QGraphicsEllipseItem):
    
    pos: QPoint
    
    def __init__(self, ellipse: QRectF = QRectF(0, 0, 0 , 0)):
        super().__init__(ellipse)


class PlayerGridWidget(QGraphicsView):
    def __init__(
        self,
        num_cells: XY = DEFAULT_GRID_CELLS,
        grid_area: QRect = DEFAULT_GRID_AREA
        ):
        super().__init__()
        
        self.setGeometry(grid_area.marginsAdded(QMargins(30,10,30,60)))
        
        # Create widgets for drawing on to scene
        self.draw_grid_widget = DrawGridWidget(num_cells, grid_area)
        self.player_item = DrawPlayerWidget()
        
        # Create and set scene
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.grid_item = self.scene.addPixmap(self.draw_grid_widget.get_pixmap())
    
    def move_player(coord: XY):
        self.scene.addEllipse(QRectF(0, 0, 20 , 20), QPen(*PEN_GRY_SML), QBrush(*BRUSH_RED_SLD))
            
    
def size_fits_in_rect(size: QSize, rect: QRect):
    return size.width() <= rect.width() and size.height() <= rect.height()
            

if __name__ == "__main__":
    app = QApplication([])
    window = PlayerGridWidget()
    window.move(QPoint(100, 100))
    window.show()
    app.exec()
