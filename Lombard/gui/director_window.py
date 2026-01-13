from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QGridLayout
)
from PyQt5.QtGui import QFont

from core.boss_engine import build_statistics
from core.app_paths import data_file

class DirectorWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Director Panel")
        self.setGeometry(500, 300, 350, 300)

        layout = QVBoxLayout()

        title = QLabel("Statistics")
        title.setFont(QFont("Arial", 16))
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

        btn = QPushButton("Update statistics")
        btn.clicked.connect(self.update_statistics)
        layout.addWidget(btn)

        self.setLayout(layout)

        # Автоматичне оновлення при відкритті
        self.update_statistics()

    def update_statistics(self):
        try:
            build_statistics()
            stats = self.read_stats()
            self.show_stats(stats)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update: {str(e)}")

    def read_stats(self):
        path = data_file("director_stat.txt")

        if not path.exists():
            raise RuntimeError(f"Statistics file not found:\n{path}")

        stats = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" not in line:
                    continue
                k, v = line.strip().split("=", 1)
                stats[k] = v
        return stats

    def show_stats(self, stats):
        """Метод для відображення статистики у лейблах"""
        for key, label in self.labels.items():
            val = stats.get(key, "0")
            if key == "total_value":
                label.setText(f"{val} грн")
            else:
                label.setText(val)