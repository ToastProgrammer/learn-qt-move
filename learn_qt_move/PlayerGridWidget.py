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

from PyQt6.QtCore import QLine, QPoint, QRect, QRectF, QSize, Qt, QMargins, QPointF
from PyQt6.QtGui import QBrush, QPainter, QPaintEvent, QPen, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt6.QtWidgets import QVBoxLayout


from common import XY
from common import BRUSH_BLU_SLD, BRUSH_RED_SLD, PEN_BLA_MED, PEN_GRY_SML
from common import GridInvalidError

from PainterUtils import OutOfBoundsError
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
    _space_size: XY
    _space_x_coords: list[int]
    _space_y_coords: list[int]
    space_coords: list[list[XY]]
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
            
            self._space_size, self._space_x_coords, self._space_y_coords = draw_grid(painter, self.grid_area, self.grid_num_cells, PEN_BLA_MED, brush_style=BRUSH_BLU_SLD)
            # Add shading detailing to grid
            draw_grid(painter, self.grid_area, self.grid_num_cells, PEN_GRY_SML, offset=XY(2,2))
            
        finally:
            painter.restore()
        painter.end()
            
        if not self._space_x_coords or not self._space_y_coords:
            raise GridInvalidError("An error occured when trying to draw the grid, as no space indices were defined.")
        
    def get_pixmap(self) -> QPixmap:
        return self.grid_pixmap
    
    def get_grid_space_size(self) -> XY:
        """Get the characteristics of the generated grid.

        Returns:
            XY: The dimensions of a square in the grid.
        """
        return self._space_size
    
    def get_space_coords(self, coords: XY) -> XY:
        """Get the XY location of specified space in grid.

        Args:
            coords (XY): location on grid to get coordinates

        Returns:
            XY: xy location of input coordinates on grid
        """
        return (self._space_x_coords[coords.x], self._space_x_coords[coords.x])


class PlayerGridWidget(QGraphicsView):
    
    scene_widget: QGraphicsScene
    draw_grid_widget: DrawGridWidget
    player_item: QGraphicsEllipseItem | None = None
    grid_item: QPixmap
    
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
    
    def move_player(self, coord: QPoint):
        
        if self.player_item:
            if not self.geometry().contains(QRect(QPoint(coord), self.player_item.rect().size().toSize())):
                raise OutOfBoundsError(coord, XY(self.geometry().x(), self.geometry().y()))
            else:
                self.player_item.setPos(coord.x(), coord.y())
        else:
            _player_size = self.draw_grid_widget.get_grid_space_size()
            self.player_item = self.scene_widget.addEllipse(
                coord.x(),
                coord.y(),
                _player_size.x, 
                _player_size.y,
                QPen(*PEN_GRY_SML),
                QBrush(*BRUSH_RED_SLD)
                )
            
    # def move_player_space(self, space: XY):
    

if __name__ == "__main__":
    app = QApplication([])
    window = PlayerGridWidget()
    window.show()
    window.move_player(QPoint(0, 0))
    app.exec()
