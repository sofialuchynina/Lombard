from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
import os
import time


class LoansWindow(QWidget):
    def __init__(self, client_id=None):
        """
        client_id:
            - якщо касир вибрав клієнта → буде передано ID
            - якщо адміністратор відкриває → None
        """

        super().__init__()

        self.client_id = client_id 
        self.setWindowTitle("Loans")
        self.setGeometry(450, 250, 650, 420)

        layout = QVBoxLayout()

        title = QLabel("Create New Loan")
        layout.addWidget(title)

        form = QHBoxLayout()

        self.client_box = QComboBox()
        self.load_clients()

        if self.client_id is not None:
            self.set_selected_client(self.client_id)
            self.client_box.setEnabled(False)  

        form.addWidget(self.client_box)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        form.addWidget(self.amount_input)

        self.percent_input = QLineEdit()
        self.percent_input.setPlaceholderText("Interest %")
        form.addWidget(self.percent_input)

        btn_create = QPushButton("Create Loan")
        btn_create.clicked.connect(self.create_loan)
        form.addWidget(btn_create)

        layout.addLayout(form)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Client", "Amount", "Percent", "Status"])
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_loans()

    def load_clients(self):
        self.client_box.clear()

        if not os.path.exists("database/clients.txt"):
            return

        with open("database/clients.txt", "r", encoding="utf-8") as f:
            next(f) 
            for line in f:
                id_, name, phone, passport = line.strip().split("|")
                self.client_box.addItem(f"{id_} — {name}")

    def set_selected_client(self, client_id):
        """
        Встановлює вибраного клієнта у пов’язаному форматі:
        'ID — Name'
        """

        for i in range(self.client_box.count()):
            item_text = self.client_box.itemText(i)
            if item_text.startswith(str(client_id) + " —"):
                self.client_box.setCurrentIndex(i)
                return

        print("[WARNING] Client ID not found:", client_id)

    def load_loans(self):
        if not os.path.exists("database/loans.txt"):
            return

        self.table.setRowCount(0)

        with open("database/loans.txt", "r", encoding="utf-8") as f:
            for line in f:
                data = line.strip().split("|")
                row = self.table.rowCount()
                self.table.insertRow(row)
                for col, value in enumerate(data):
                    self.table.setItem(row, col, QTableWidgetItem(value))

    def create_loan(self):
        try:
            client = self.client_box.currentText()
            amount = float(self.amount_input.text())
            percent = float(self.percent_input.text())
        except:
            QMessageBox.warning(self, "Error", "Check input numbers!")
            return

        loan_id = str(int(time.time())) 
        status = "active"

        rowdata = [loan_id, client, str(amount), str(percent), status]

        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, val in enumerate(rowdata):
            self.table.setItem(row, col, QTableWidgetItem(val))

        with open("database/loans.txt", "a", encoding="utf-8") as f:
            f.write("|".join(rowdata) + "\n")

        self.amount_input.clear()
        self.percent_input.clear()

        QMessageBox.information(self, "Success", "Loan created!")
