from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from core.app_paths import data_file

class LoginWindow(QWidget):
    def __init__(self, app_reference):
        super().__init__()
        self.app_reference = app_reference

        self.setWindowTitle("Authorization")
        self.setGeometry(500, 300, 350, 200)

        layout = QVBoxLayout()
        title = QLabel("System Login")
        title.setFont(QFont("Arial", 16))

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Login")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        btn = QPushButton("Sign In")
        btn.clicked.connect(self.check_login)

        layout.addWidget(title)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)
        layout.addWidget(btn)
        self.setLayout(layout)

    def check_login(self):
        users_path = data_file("users.txt")
        if not users_path.exists():
            QMessageBox.critical(self, "Error", "users.txt not found")
            return

        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        with open(users_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        start_index = 1 if lines and "user" in lines[0].lower() else 0

        for line in lines[start_index:]:
            parts = line.strip().split("|")
            if len(parts) == 3:
                user, pwd, role = parts
                if user == login and pwd == password:
                    self.app_reference.current_role = role
                    self.app_reference.show_main_window() 
                    self.close()
                    return

        QMessageBox.warning(self, "Error", "Invalid login or password")