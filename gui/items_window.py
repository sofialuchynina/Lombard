from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox,
    QLineEdit, QDialog
)
from core.receipt_generator import generate_receipt
from core.app_paths import data_file


class AddItemWindow(QDialog):
    def __init__(self, parent=None, mode="buy"):
        super().__init__(parent)
        self.mode = mode

        self.setWindowTitle("Новий товар")
        self.setGeometry(500, 300, 300, 150)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Назва товару")
        layout.addWidget(self.name_input)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Ціна")
        layout.addWidget(self.price_input)

        btn_ok = QPushButton("Додати")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

        self.setLayout(layout)

    def get_data(self):
        return self.name_input.text().strip(), self.price_input.text().strip()


class ItemsWindow(QWidget):
    def __init__(self, client_id=None, client_name=None):
        super().__init__()

        self.client_id = client_id
        self.client_name = client_name

        self.setWindowTitle("Pawn Shop – Items")
        self.setGeometry(450, 250, 750, 450)

        layout = QVBoxLayout()

        title = QLabel("Items & Operations")
        layout.addWidget(title)

        if self.client_name:
            layout.addWidget(QLabel(f"Client: {self.client_name}"))

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Status"])
        layout.addWidget(self.table)

        self.load_items()

        btn_layout = QHBoxLayout()

        btn_buy = QPushButton("Купити товар (додати новий)")
        btn_sell = QPushButton("Продати товар")
        btn_pawn = QPushButton("Прийняти заставу")
        btn_return = QPushButton("Повернути заставу")

        btn_buy.clicked.connect(self.buy_item)
        btn_sell.clicked.connect(self.sell_item)
        btn_pawn.clicked.connect(self.pawn_item)
        btn_return.clicked.connect(self.return_item)

        btn_layout.addWidget(btn_buy)
        btn_layout.addWidget(btn_sell)
        btn_layout.addWidget(btn_pawn)
        btn_layout.addWidget(btn_return)

        layout.addLayout(btn_layout)
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
            line = line.strip()
            if not line:
                continue

            parts = line.split("|")
            if len(parts) != 4:
                continue

            item_id, name, price, status = parts

            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(item_id))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(price))
            self.table.setItem(row, 3, QTableWidgetItem(status))

    def save_all(self):
        path = self.items_file()
        with open(path, "w", encoding="utf-8") as f:
            f.write("id|name|price|status\n")
            for row in range(self.table.rowCount()):
                values = [self.table.item(row, col).text() for col in range(4)]
                f.write("|".join(values) + "\n")

    def buy_item(self):
        dialog = AddItemWindow(self, mode="buy")
        if dialog.exec_() != QDialog.Accepted:
            return

        name, price = dialog.get_data()
        if not name or not price:
            QMessageBox.warning(self, "Error", "Заповніть всі поля!")
            return

        new_id = str(self.table.rowCount() + 1)

        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(new_id))
        self.table.setItem(row, 1, QTableWidgetItem(name))
        self.table.setItem(row, 2, QTableWidgetItem(price))
        self.table.setItem(row, 3, QTableWidgetItem("в наявності"))

        self.save_all()

        generate_receipt("Купівля товару", name, price, self.client_name)
        QMessageBox.information(self, "Success", "Новий товар додано!")

    def pawn_item(self):
        dialog = AddItemWindow(self, mode="pawn")
        if dialog.exec_() != QDialog.Accepted:
            return

        name, price = dialog.get_data()
        if not name or not price:
            QMessageBox.warning(self, "Error", "Заповніть всі поля!")
            return

        new_id = str(self.table.rowCount() + 1)

        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(new_id))
        self.table.setItem(row, 1, QTableWidgetItem(name))
        self.table.setItem(row, 2, QTableWidgetItem(price))
        self.table.setItem(row, 3, QTableWidgetItem("застава"))

        self.save_all()

        generate_receipt("Прийом застави", name, price, self.client_name)
        QMessageBox.information(self, "Success", "Заставу прийнято!")

    def sell_item(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Select an item!")
            return

        if self.table.item(row, 3).text() != "в наявності":
            QMessageBox.warning(self, "Error", "Товар недоступний для продажу!")
            return

        name = self.table.item(row, 1).text()
        price = self.table.item(row, 2).text()

        self.table.setItem(row, 3, QTableWidgetItem("продано"))
        self.save_all()

        generate_receipt("Продаж товару", name, price, self.client_name)
        QMessageBox.information(self, "Success", "Товар продано!")

    def return_item(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Виберіть товар!")
            return

        if self.table.item(row, 3).text() != "застава":
            QMessageBox.warning(self, "Error", "Цей товар не є заставою!")
            return

        name = self.table.item(row, 1).text()
        price = self.table.item(row, 2).text()

        self.table.setItem(row, 3, QTableWidgetItem("повернено клієнту"))
        self.save_all()

        generate_receipt("Повернення застави", name, price, self.client_name)
        QMessageBox.information(self, "Success", "Заставу повернено!")
