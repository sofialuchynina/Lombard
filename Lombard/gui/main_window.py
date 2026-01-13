from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QFont
from core.app_paths import data_file

class MainWindow(QWidget):
    def __init__(self, role, app_reference):
        super().__init__()

        self.role = role
        self.app_reference = app_reference

        self.setWindowTitle(f"Lombard System — {role.capitalize()}")
        self.setGeometry(400, 200, 450, 500)

        self.selected_client_id = None
        self.selected_client_name = None

        layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        title = QLabel("Main Menu")
        title.setFont(QFont("Arial", 18))
        
        btn_logout = QPushButton("Log Out")
        btn_logout.setFixedWidth(90)

        btn_logout.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold;")
        btn_logout.clicked.connect(self.handle_logout)
        
        top_bar.addWidget(title)
        top_bar.addStretch()
        top_bar.addWidget(btn_logout)
        layout.addLayout(top_bar)

        logged_info = QLabel(f"Logged as: {role}")
        logged_info.setFont(QFont("Arial", 12))
        layout.addWidget(logged_info)

        if role == "director":
            btn_director = QPushButton("Open Director Panel")
            btn_director.clicked.connect(self.open_director_panel)
            layout.addWidget(btn_director)

        if role == "administrator":
            btn_clients = QPushButton("Clients")
            btn_clients.clicked.connect(self.open_clients)
            btn_items = QPushButton("Items Editor")
            btn_items.clicked.connect(self.open_items_admin)
            layout.addWidget(btn_clients)
            layout.addWidget(btn_items)

        if role == "cashier":
            btn_clients = QPushButton("Clients (View Only)")
            btn_clients.clicked.connect(self.open_clients)
            btn_items = QPushButton("Items (Buy / Sell / Pawn)")
            btn_items.clicked.connect(self.open_items)
            btn_receipts = QPushButton("Receipts")
            btn_receipts.clicked.connect(self.open_receipts)
            layout.addWidget(btn_clients)
            layout.addWidget(btn_items)
            layout.addWidget(btn_receipts)

        btn_exit = QPushButton("Exit System")
        btn_exit.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold;")
        btn_exit.clicked.connect(self.close)
        layout.addWidget(btn_exit)

        self.setLayout(layout)

    def handle_logout(self):
        """Метод для виходу з облікового запису"""
        reply = QMessageBox.question(self, 'Logout', "Are you sure you want to log out?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.app_reference.logout() 

    def clients_path(self):
        p = data_file("clients.txt")
        if not p.exists():
            p.write_text("id|name|phone|passport\n", encoding="utf-8")
        return p

    def open_clients(self):
        from gui.clients_window import ClientsWindow
        callback = self.client_selected_for_items if self.role == "cashier" else None
        self.clients_window = ClientsWindow(role=self.role, callback_select=callback)
        self.clients_window.show()

    def open_items(self):
        path = self.clients_path()
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) <= 1:
            QMessageBox.information(self, "No clients", "Client database is empty.")
            return
        from gui.clients_window import ClientsWindow
        self.clients_window = ClientsWindow(role="cashier", callback_select=self.client_selected_for_items)
        self.clients_window.show()

    def client_selected_for_items(self, client_id):
        self.selected_client_id = client_id
        path = self.clients_path()
        with open(path, "r", encoding="utf-8") as f:
            next(f, None)
            for line in f:
                parts = line.strip().split("|")
                if parts[0] == client_id:
                    self.selected_client_name = parts[1]
                    break
        self.open_items_window()

    def open_items_window(self):
        from gui.items_window import ItemsWindow
        self.items_window = ItemsWindow(client_id=self.selected_client_id, client_name=self.selected_client_name)
        self.items_window.show()

    def open_items_admin(self):
        from gui.admin_items_window import AdminItemsWindow
        self.items_window = AdminItemsWindow()
        self.items_window.show()

    def open_director_panel(self):
        from gui.director_window import DirectorWindow
        self.dir_win = DirectorWindow()
        self.dir_win.show()

    def open_receipts(self):
        from gui.receipts_window import ReceiptsWindow
        self.receipts_window = ReceiptsWindow()
        self.receipts_window.show()