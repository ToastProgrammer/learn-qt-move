from contextlib import contextmanager
from typing import Tuple, List, Optional

from PyQt6.QtCore import QLine, QPoint, QRect, QSize, Qt, QMargins
from PyQt6.QtGui import QBrush, QPainter, QPaintEvent, QPen
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QVBoxLayout

from common import PenConfig, BrushConfig
from common import XY


def draw_grid(
    painter: QPainter,
    area: QRect,
    num_cells: XY,
    pen_style: QPen,
    offset: XY = XY(0,0),
    brush_style: Optional[QBrush] = None,
    ) -> Tuple[List[QPoint]]:

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
        for h in range(1,num_cells.x):
            pos = area.width() // num_cells.x * h + area.left() + offset.x
            x_pos.append(pos)
            painter.drawLine(
                QPoint(pos, area.top()),    # (x,y)
                QPoint(pos, area.bottom())  # (dx,dy)
                )
                
        # Draw Horizontal lines for Rows
        for v in range(1,num_cells.y):
            pos = area.height() // num_cells.y * v + area.top() + offset.y
            y_pos.append(pos)
            painter.drawLine(
                QPoint(area.left(), pos), 
                QPoint(area.right(), pos)
                )
    finally:
        painter.restore()
        
    return (x_pos, y_pos)