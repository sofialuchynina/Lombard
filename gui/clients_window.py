from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
)
from core.app_paths import data_file


class ClientsWindow(QWidget):
    def __init__(self, role="cashier", callback_select=None, force_add=False):
        super().__init__()

        self.role = role
        self.callback_select = callback_select
        self.force_add = force_add

        self.setWindowTitle("Clients")
        self.setGeometry(450, 250, 650, 450)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Passport"])
        layout.addWidget(self.table)

        form = QHBoxLayout()
        self.name_input = QLineEdit(); self.name_input.setPlaceholderText("Name")
        self.phone_input = QLineEdit(); self.phone_input.setPlaceholderText("Phone")
        self.passport_input = QLineEdit(); self.passport_input.setPlaceholderText("Passport")
        form.addWidget(self.name_input)
        form.addWidget(self.phone_input)
        form.addWidget(self.passport_input)
        layout.addLayout(form)

        btns = QHBoxLayout()
        self.btn_add = QPushButton("Add")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")
        self.btn_select = QPushButton("Select Client")

        self.btn_add.clicked.connect(self.add_client)
        self.btn_edit.clicked.connect(self.edit_client)
        self.btn_delete.clicked.connect(self.delete_client)
        self.btn_select.clicked.connect(self.select_client)

        btns.addWidget(self.btn_add)
        btns.addWidget(self.btn_edit)
        btns.addWidget(self.btn_delete)
        btns.addWidget(self.btn_select)
        layout.addLayout(btns)

        self.setLayout(layout)

        self.load_clients()
        self.apply_permissions()

        if self.force_add and self.role == "cashier":
            QMessageBox.information(self, "Info", "Please add a new client using Administrator role.")

    def clients_file(self):
        path = data_file("clients.txt")
        if not path.exists():
            path.write_text("id|name|phone|passport\n", encoding="utf-8")
        return path

    def apply_permissions(self):
        if self.role == "administrator":
            self.btn_select.hide()
        else:
            self.btn_add.hide()
            self.btn_edit.hide()
            self.btn_delete.hide()

    def load_clients(self):
        path = self.clients_file()

        self.table.setRowCount(0)

        with open(path, "r", encoding="utf-8") as f:
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
        if self.role != "administrator":
            return

        path = self.clients_file()

        with open(path, "w", encoding="utf-8") as f:
            f.write("id|name|phone|passport\n")
            for row in range(self.table.rowCount()):
                values = [self.table.item(row, c).text() for c in range(4)]
                f.write("|".join(values) + "\n")

    def add_client(self):
        if self.role != "administrator":
            return

        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        passport = self.passport_input.text().strip()

        if not all([name, phone, passport]):
            QMessageBox.warning(self, "Error", "Fill all fields!")
            return

        row = self.table.rowCount()
        new_id = str(row + 1)

        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(new_id))
        self.table.setItem(row, 1, QTableWidgetItem(name))
        self.table.setItem(row, 2, QTableWidgetItem(phone))
        self.table.setItem(row, 3, QTableWidgetItem(passport))

        self.save_all()

        self.name_input.clear()
        self.phone_input.clear()
        self.passport_input.clear()

    def edit_client(self):
        if self.role != "administrator":
            return

        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Select client!")
            return

        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        passport = self.passport_input.text().strip()

        if name:
            self.table.setItem(row, 1, QTableWidgetItem(name))
        if phone:
            self.table.setItem(row, 2, QTableWidgetItem(phone))
        if passport:
            self.table.setItem(row, 3, QTableWidgetItem(passport))

        self.save_all()

    def delete_client(self):
        if self.role != "administrator":
            return

        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Select client!")
            return

        self.table.removeRow(row)
        self.save_all()

    def select_client(self):
        if self.role != "cashier":
            return

        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Select client!")
            return

        if self.callback_select:
            client_id = self.table.item(row, 0).text()
            self.callback_select(client_id)
            self.close()
