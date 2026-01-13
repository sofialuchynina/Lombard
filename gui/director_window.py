import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QGridLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QHeaderView, QDialog
)
from PyQt5.QtGui import QFont

from core.boss_engine import build_statistics, detect_anomalies, sort_items_by_price
from core.app_paths import data_file

class ReportViewer(QDialog):
    """Вікно для відображення результатів аналізу у вигляді таблиці"""
    def __init__(self, title, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(700, 500)
        
        layout = QVBoxLayout(self)
        
        # Створюємо таблицю
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        self.load_data(file_path)

    def load_data(self, file_path):
        if not os.path.exists(file_path):
            return

        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        if not lines:
            return

        # Читаємо заголовки з першого рядка (id|name|price|status)
        headers = lines[0].split("|")
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Заповнюємо дані
        data_lines = lines[1:]
        self.table.setRowCount(len(data_lines))
        
        for row_idx, line in enumerate(data_lines):
            columns = line.split("|")
            for col_idx, text in enumerate(columns):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(text))
        
        # Розтягуємо колонки
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

class DirectorWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Director Panel (C++ Powered)")
        self.setGeometry(500, 300, 450, 500)

        layout = QVBoxLayout()

        title = QLabel("System Statistics")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)

        self.grid = QGridLayout()
        layout.addLayout(self.grid)

        self.labels = {}
        rows = [
            ("Total items", "total"),
            ("Available", "available"),
            ("Sold", "sold"),
            ("Pawned", "pawn"),
            ("Returned", "returned"),
            ("Total value", "total_value"),
        ]

        for row, (text, key) in enumerate(rows):
            name = QLabel(text + ":")
            value = QLabel("-")
            name.setFont(QFont("Arial", 11))
            value.setFont(QFont("Arial", 11))
            self.grid.addWidget(name, row, 0)
            self.grid.addWidget(value, row, 1)
            self.labels[key] = value

        self.btn_stats = QPushButton("Update Statistics")
        self.btn_stats.setStyleSheet("background-color: #e1f5fe; height: 35px; font-weight: bold;")
        self.btn_stats.clicked.connect(self.update_statistics)
        layout.addWidget(self.btn_stats)

        layout.addSpacing(20)
        layout.addWidget(QLabel("Advanced C++ Analysis:"))
        
        self.btn_anomaly = QPushButton("View Price Anomalies")
        self.btn_anomaly.setStyleSheet("height: 30px;")
        self.btn_anomaly.clicked.connect(self.run_anomaly_detection)
        layout.addWidget(self.btn_anomaly)

        layout.addWidget(QLabel("Sorting Tools:"))
        sort_layout = QHBoxLayout()
        self.btn_sort_asc = QPushButton("Price: Low to High")
        self.btn_sort_asc.clicked.connect(lambda: self.run_sort(True))
        
        self.btn_sort_desc = QPushButton("Price: High to Low")
        self.btn_sort_desc.clicked.connect(lambda: self.run_sort(False))
        
        sort_layout.addWidget(self.btn_sort_asc)
        sort_layout.addWidget(self.btn_sort_desc)
        layout.addLayout(sort_layout)

        self.setLayout(layout)
        self.update_statistics()

    def update_statistics(self):
        try:
            if build_statistics():
                stats = self.read_stats()
                self.show_stats(stats)
            else:
                raise RuntimeError("C++ build_statistics failed")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update: {str(e)}")

    def run_anomaly_detection(self):
        if detect_anomalies(factor=1.5):
            path = data_file("anomalies.txt")
            viewer = ReportViewer("Anomaly Report (C++)", str(path), self)
            viewer.exec_()
        else:
            QMessageBox.warning(self, "Error", "C++ anomaly detection failed.")

    def run_sort(self, asc):
        if sort_items_by_price(ascending=asc):
            path = data_file("sorted_items.txt")
            viewer = ReportViewer("Sorted Inventory (C++)", str(path), self)
            viewer.exec_()
        else:
            QMessageBox.warning(self, "Error", "C++ sorting failed.")

    def read_stats(self):
        path = data_file("director_stat.txt")
        if not path.exists():
            raise RuntimeError(f"Statistics file not found:\n{path}")
        stats = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    stats[k] = v
        return stats

    def show_stats(self, stats):
        for key, label in self.labels.items():
            val = stats.get(key, "0")
            if key == "total_value":
                label.setText(f"{val} грн")
            else:
                label.setText(val)