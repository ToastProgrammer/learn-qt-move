"""
"""
from __future__ import annotations

from dataclasses import dataclass

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize
from PyQt6.QtCore import QRect


@dataclass
class XY:
    x: int
    y: int

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


DEFAULT_GRID_SIZE = QSize(340, 380)

DEFAULT_CANVAS_RECT = QRect(20, 20, 300, 300)

# QPen Configurations
PEN_BLACK_MEDIUM = PenConfig(Qt.GlobalColor.black, 5, Qt.PenStyle.SolidLine)

# QBrush Configurations
BRUSH_BLUE_SOLID = BrushConfig(Qt.GlobalColor.cyan, Qt.BrushStyle.SolidPattern)