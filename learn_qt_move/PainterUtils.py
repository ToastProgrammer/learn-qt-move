from contextlib import contextmanager
from typing import Tuple, List, Optional, Union

from PyQt6.QtCore import QLine, QPoint, QRect, QSize, Qt, QMargins
from PyQt6.QtGui import QBrush, QPainter, QPaintEvent, QPen, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QVBoxLayout

from common import PenConfig, BrushConfig
from common import XY


@contextmanager
def qpainter_config(painter: QPainter):
    painter.save()
    try:
        yield painter
    finally:
        painter.restore()


def draw_grid(
    painter: QPainter,
    area: QRect | QPixmap,
    num_cells: XY,
    pen_style: QPen,
    offset: XY = XY(0,0),
    brush_style: Optional[QBrush] = None,
    ) -> Tuple[XY, Tuple[QPoint, ...]]:

    x_pos: List[int] = []
    y_pos: List[int] = []
    
    painter.save()
    
    try:
        # Grid Line style
        painter.setPen(QPen(*pen_style))
        
        # Background style if used
        if brush_style:
            painter.setBrush(QBrush(*brush_style))
            painter.drawRect(area)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
        
        # Draw Vertical Lines for Columns
        h_len = area.width() // num_cells.x
        for h in range(1,num_cells.x):
            pos = h_len * h + area.left() + offset.x
            x_pos.append(pos)
            painter.drawLine(
                QPoint(pos, area.top()),    # (x,y)
                QPoint(pos, area.bottom())  # (dx,dy)
                )
                
        # Draw Horizontal lines for Rows
        v_len = area.height() // num_cells.y
        for v in range(1,num_cells.y):
            pos = v_len * v + area.top() + offset.y
            y_pos.append(pos)
            painter.drawLine(
                QPoint(area.left(), pos), 
                QPoint(area.right(), pos)
                )
    finally:
        painter.restore()
        
    return (XY(h_len, v_len), x_pos, y_pos)