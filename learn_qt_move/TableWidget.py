from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QHBoxLayout, QTableWidgetItem

# from: https://doc.qt.io/qtforpython-6/tutorials/expenses/expenses.html

FILE_TABS = ["Open", "New Tab", "Close Tab"]


class DataTableWidget(QWidget):
    table_size: int = 0

    def __init__(self):
        super().__init__()
        
        # Example data
        self._data = { 
            "Water": 24.5, "Electricity": 55.1, "Rent": 850.0,
            "Supermarket": 230.4, "Internet": 29.99, "Bars": 21.85,
            "Public transportation": 60.0, "Coffee": 22.45, "Restaurants": 120
            }
            
        # Left
        self.table = QTableWidget()
        self.table.setColumnCount(2) 
        self.table.setHorizontalHeaderLabels(["Description", "Price"])
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView)

        # QWidget Layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.table)

        # Fill example data
        self.fill_table()

    def fill_table(self, data_in=None):
        data = data_in or self._data
        i = 0
        for obj, val in data.items():
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(obj)))
            self.table.setItem(i, 1, QTableWidgetItem(str(val)))
            i += 1


class MultiTabWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.data_table = DataTableWidget()


        self.setWindowTitle("Multi-Tab Window")
        self.resize(800, 600)

        
        self.setCentralWidget(self.data_table)


def main():
    app = QApplication([])
    window = MultiTabWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
