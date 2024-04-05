"""
"""
from __future__ import annotations

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
            # Add shading detailing to grid
            draw_grid(painter, self.grid_area, self.grid_num_cells, PEN_GRY_SML, offset=XY(2,2))
            
        finally:
            painter.restore()
        painter.end()
            
        if not self.grid_details:
            raise GridInvalidError("An error occured when trying to draw the g rid, as no space indices were defined.")
        
    def get_pixmap(self) -> QPixmap:
        return self.grid_pixmap
    
    def get_grid_space_details(self) -> tuple[XY, list[int], list[int]]:
        """
        Get the characteristics of the generated grid.

        Returns:
            tuple[XY, list[int], list[int]]: The dimensions of a square in the grid, and each x and y position of a line in the grid.
        """
        return self.grid_details
        

class DrawPlayerWidget(QGraphicsEllipseItem):
    
    pos: QPoint
    
    def __init__(self, ellipse: QRectF = QRectF(0, 0, 0 , 0)):
        super().__init__(ellipse)


class PlayerGridWidget(QGraphicsView):
    
    scene_widget: QGraphicsScene
    draw_grid_widget: DrawGridWidget
    player_item: QGraphicsEllipseItem | None
    grid_item: QPixmap
    
    grid_space_coords: tuple
    
    def __init__(
        self,
        num_cells: XY = DEFAULT_GRID_CELLS,
        grid_area: QRect = DEFAULT_GRID_AREA
        ):
        super().__init__()
        
        self.setGeometry(grid_area.marginsAdded(QMargins(30,10,30,60)))
        
        # Create widgets for drawing on to scene
        self.draw_grid_widget = DrawGridWidget(num_cells, grid_area)
        
        # Create and set scene
        self.scene_widget = QGraphicsScene(self)
        self.setScene(self.scene_widget)
        
        self.grid_item = self.scene_widget.addPixmap(self.draw_grid_widget.get_pixmap())
        self.player_item = None
    
    def move_player(self, coord: XY):
        
        if self.player_item:
            if (
                coord.x + self.player_item.rect().width() > self.geometry().x or 
                coord.y + self.player_item.rect().height() > self.geometry().y
                ):
                print(
                    f"Could not move player to ({coord.x}, {coord.y}) as it is outside the boundary"
                    f"({self.geometry().x}, {self.geometry().y})"
                    )
            else:
                self.player_item.setPos(coord.x, coord.y)
        else:
            self.player_item = self.scene_widget.addEllipse(coord.x, coord.y, self.draw_grid_widget.grid_details[0].x, self.draw_grid_widget.grid_details[0].y, QPen(*PEN_GRY_SML), QBrush(*BRUSH_RED_SLD))
            
    def move_player_by(self, vec: XY):
        if not self.player_item:
            print(f"Could not move player by {vec} as no player was created.")
        else:
            self.move_player(self.player_item.x + vec.x, self.player_item.y + vec.y)
            
    # def move_to_space(self, space: XY):
        
            
    
def size_fits_in_rect(size: QSize, rect: QRect):
    return size.width() <= rect.width() and size.height() <= rect.height()
            

if __name__ == "__main__":
    app = QApplication([])
    window = PlayerGridWidget()
    window.show()
    window.move_player(XY(0, 0))
    app.exec()
