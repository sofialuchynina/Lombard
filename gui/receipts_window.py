from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QListWidget, QTextEdit, QMessageBox, QLabel, QFileDialog
)
from PyQt5.QtGui import QFont
from core.app_paths import data_file
from core.receipt_generator import export_to_pdf

class ReceiptsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Receipts")
        self.setGeometry(400, 200, 800, 500)

        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        title = QLabel("Receipts")
        title.setFont(QFont("Arial", 14))
        left_layout.addWidget(title)

        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self.show_receipt)
        left_layout.addWidget(self.list_widget)

        right_layout = QVBoxLayout()
        text_title = QLabel("Receipt preview")
        text_title.setFont(QFont("Arial", 14))
        right_layout.addWidget(text_title)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        right_layout.addWidget(self.text_edit)

        self.btn_pdf = QPushButton("Зберегти у PDF")
        self.btn_pdf.setFixedHeight(40)
        self.btn_pdf.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold;")
        self.btn_pdf.clicked.connect(self.save_as_pdf)
        right_layout.addWidget(self.btn_pdf)

        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 3)
        self.setLayout(main_layout)

        self.receipts = []
        self.load_receipts()

    def load_receipts(self):
        path = data_file("recipes.txt")
        if not path.exists():
            return
        content = path.read_text(encoding="utf-8")
        blocks = content.split("========================================")
        self.receipts = [b.strip() for b in blocks if b.strip()]
        self.list_widget.clear()
        for block in self.receipts:
            self.list_widget.addItem(self.extract_title(block))

    def extract_title(self, block: str) -> str:
        data = self.parse_block(block)
        return f"{data['date']} | {data['client']} | {data['op']}"

    def parse_block(self, block: str) -> dict:
        """Перетворює текст блоку у зручний словник"""
        lines = block.splitlines()
        res = {"date": "?", "client": "?", "op": "?", "item": "?", "sum": "?"}
        for l in lines:
            if "Дата:" in l: res["date"] = l.split(":", 1)[1].strip()
            elif "Клієнт:" in l: res["client"] = l.split(":", 1)[1].strip()
            elif "Операція:" in l: res["op"] = l.split(":", 1)[1].strip()
            elif "Товар:" in l: res["item"] = l.split(":", 1)[1].strip()
            elif "Сума:" in l: res["sum"] = l.split(":", 1)[1].strip()
        return res

    def show_receipt(self, index):
        if 0 <= index < len(self.receipts):
            self.text_edit.setPlainText(self.receipts[index])

    def save_as_pdf(self):
        idx = self.list_widget.currentRow()
        if idx < 0:
            QMessageBox.warning(self, "Помилка", "Виберіть квитанцію!")
            return

        data = self.parse_block(self.receipts[idx])
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Зберегти PDF", f"Receipt_{data['date'].replace(':','-')}.pdf", "PDF Files (*.pdf)"
        )

        if file_path:
            try:
                export_to_pdf(data, file_path)
                QMessageBox.information(self, "Успіх", "PDF файл успішно створено!")
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Не вдалося створити PDF: {str(e)}")