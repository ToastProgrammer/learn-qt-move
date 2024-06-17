from dataclasses import dataclass
from typing import Any
from typing import Collection
from typing import Optional

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QTableWidgetItem

from common import XY


# from: https://doc.qt.io/qtforpython-6/tutorials/expenses/expenses.html


FILE_TABS = ["Open", "New Tab", "Close Tab"]
TEST_DATA = [
    ("Place", XY(0,0)), ("Move", XY(0,1)), ("Move", XY(1,1)),
    ("Move", XY(1,0)), ("Move", XY(4,0)), ("Move", XY(4,4)),
    ("Move", XY(3,4)), ("Move", XY(3,3)), ("Move", XY(0,3))
]


class DataTableWidget(QWidget):
    """
    
    """
    table_size: int = 0
    stored_data: Optional[Collection]

    def __init__(
            self,
            data: list[tuple[Any, Any]],
            headers: Collection[str] = ["Event", "Description"]
            ):
        super().__init__()
        
        # Example data
        self.stored_data = data
            
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # QWidget Layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.table)

        # Fill example data
        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)   # Clear the table
        for it, (obj, val) in enumerate(self.stored_data):
            self.table.insertRow(it)
            self.table.setItem(it, 0, QTableWidgetItem(str(obj)))   # Column 1
            self.table.setItem(it, 1, QTableWidgetItem(str(val)))   # Column 2


class MoveSpaceWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.data_table = DataTableWidget(data)


        self.setWindowTitle("Multi-Tab Window")
        self.resize(800, 600)

        
        self.setCentralWidget(self.data_table)


def main():
    app = QApplication([])
    window = MoveSpaceWindow(TEST_DATA)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()

