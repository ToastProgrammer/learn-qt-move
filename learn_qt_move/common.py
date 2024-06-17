"""
"""
from __future__ import annotations

from dataclasses import dataclass

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


@dataclass
class XY:
    x: int
    y: int
    
    def __add__(self, rhs: XY):
        return XY(self.x + rhs.x, self.y + rhs.y)
    
    def __sub__(self, rhs: XY):
        return XY(self.x - rhs.x, self.y - rhs.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        return(f"({self.x}, {self.y})")
    
    def __lt__(self, rhs: XY):
        return self.x < rhs.x and self.y < rhs.y
    
    def __gt__(self, rhs: XY):
        return self.x > rhs.x and self.y > rhs.y
    
    def __eq__(self, rhs: XY):
        return self.x == rhs.x and self.y == rhs.y
    
    def __le__(self, rhs: XY):
        return self.x <= rhs.x and self.y <= rhs.y
    
    def __ge__(self, rhs: XY):
        return self.x >= rhs.x and self.y >= rhs.y
    

@dataclass(frozen=True)
class PenConfig:
    color: Qt.GlobalColor
    width: int
    style: Qt.PenStyle

    def __iter__(self):
        yield self.color
        yield self.width
        yield self.style


@dataclass(frozen=True)
class BrushConfig:
    color: Qt.GlobalColor
    style: Qt.BrushStyle


    def __iter__(self):
        yield self.color
        yield self.style


class GridInvalidError(ValueError):
    pass


# QPen Configurations
PEN_BLA_MED = PenConfig(Qt.GlobalColor.black, 5, Qt.PenStyle.SolidLine)
PEN_GRY_SML = PenConfig(QColor(170, 181,198), 2, Qt.PenStyle.SolidLine)

# QBrush Configurations
BRUSH_BLU_SLD = BrushConfig(Qt.GlobalColor.cyan, Qt.BrushStyle.SolidPattern)
BRUSH_RED_SLD = BrushConfig(Qt.GlobalColor.red, Qt.BrushStyle.SolidPattern)