"""
"""
from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QPoint, QRect, QSize, QMargins
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QBrush, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem

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
        return (self._space_x_coords[coords.x], self._space_y_coords[coords.y])


class PlayerGridWidget(QGraphicsView):


    debug_msg_signal: pyqtSignal = pyqtSignal(str)

    scene_widget: QGraphicsScene
    draw_grid_widget: DrawGridWidget

    grid_item: QPixmap
    player_item: QGraphicsEllipseItem | None = None

    cur_player_space: XY

    def eprint(self, msg: str):
        self.debug_msg_signal.emit(msg)

    def __init__(
        self,
        num_cells: XY = DEFAULT_GRID_CELLS,
        grid_area: QRect = DEFAULT_GRID_AREA
        ):
        super().__init__()

        # Signals
        # self.debug_msg_signal = pyqtSignal(str)

        # Geometry
        self.setGeometry(grid_area.marginsAdded(QMargins(30,10,30,60)))

        # Create widgets for drawing on to scene
        self.draw_grid_widget = DrawGridWidget(num_cells, grid_area)
        self.scene_widget = QGraphicsScene(self)
        self.setScene(self.scene_widget)

        self.grid_item = self.scene_widget.addPixmap(self.draw_grid_widget.get_pixmap())
        # Initial conditions
        self.move_player_to_space(XY(0,0))

    def move_player(self, coord: QPoint):
        self.eprint(f"Coord: {coord}")
        self.eprint(f"Geometry: {self.geometry()}")
        _translated = coord + self.geometry().topLeft()
        if self.player_item:
            if not self.geometry().contains(_translated):
                raise OutOfBoundsError(_translated, XY(self.geometry().x(), self.geometry().y()))
            else:
                self.player_item.setPos(coord.toPointF())
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

    def move_player_to_space(self, space: XY):

        self.eprint(f"- Moving player to space: {space}")
        try:
            self.move_player(QPoint(*self.draw_grid_widget.get_space_coords(space)))
            self.eprint(f"MOVED to space: {space}")

        except (OutOfBoundsError, IndexError):
            self.eprint(f"COULD NOT move to space: {space}")

        else:
            self.cur_player_space = space

    def move_player_by_space(self, dir: str):
        _move = XY(0,0)
        if dir == "up":
           _move.y -= 1
        elif dir == "down":
            _move.y += 1
        elif dir == "left":
            _move.x -= 1
        elif dir == "right":
            _move.x += 1

        self.debug_msg_signal.emit(f"Moving player {dir} - {_move}")
        self.move_player_to_space(self.cur_player_space + _move)

        self.debug_msg_signal.emit("\n\n")


if __name__ == "__main__":
    app = QApplication([])
    window = PlayerGridWidget()
    window.show()
    window.move_player_to_space(XY(0, 0))
    app.exec()
