from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox,
    QLineEdit, QComboBox
)
from core.app_paths import data_file


class AdminItemsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin — Items Editor")
        self.setGeometry(450, 250, 650, 450)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Items (Admin Mode)"))

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Status"])
        layout.addWidget(self.table)

        self.load_items()

        form = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("New name")

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("New price")

        self.status_box = QComboBox()
        self.status_box.addItems(["в наявності", "продано", "застава", "повернено клієнту"])

        form.addWidget(self.name_input)
        form.addWidget(self.price_input)
        form.addWidget(self.status_box)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_update = QPushButton("Update selected")
        btn_delete = QPushButton("Delete selected")
        btn_update.clicked.connect(self.update_item)
        btn_delete.clicked.connect(self.delete_item)
        btns.addWidget(btn_update)
        btns.addWidget(btn_delete)
        layout.addLayout(btns)

        self.setLayout(layout)

    def items_file(self):
        path = data_file("items.txt")
        if not path.exists():
            path.write_text("id|name|price|status\n", encoding="utf-8")
        return path

    def load_items(self):
        self.table.setRowCount(0)
        path = self.items_file()

        with open(path, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()

        start_index = 1 if lines else 0

        for line in lines[start_index:]:
            parts = line.strip().split("|")
            if len(parts) != 4:
                continue

            row = self.table.rowCount()
            self.table.insertRow(row)

            for col, val in enumerate(parts):
                self.table.setItem(row, col, QTableWidgetItem(val))

    def save_all(self):
        path = self.items_file()
        with open(path, "w", encoding="utf-8") as f:
            f.write("id|name|price|status\n")
            for row in range(self.table.rowCount()):
                row_data = [self.table.item(row, col).text() for col in range(4)]
                f.write("|".join(row_data) + "\n")

    def update_item(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Select item first!")
            return

        name = self.name_input.text().strip()
        price = self.price_input.text().strip()
        status = self.status_box.currentText()

        if name:
            self.table.setItem(row, 1, QTableWidgetItem(name))
        if price:
            self.table.setItem(row, 2, QTableWidgetItem(price))

        self.table.setItem(row, 3, QTableWidgetItem(status))

        self.save_all()
        QMessageBox.information(self, "OK", "Item updated!")

    def delete_item(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Select item first!")
            return

        self.table.removeRow(row)
        self.save_all()
        QMessageBox.information(self, "Deleted", "Item removed!")
