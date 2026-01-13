from PyQt5.QtWidgets import QApplication
from gui.login_window import LoginWindow
from gui.main_window import MainWindow
import sys
import shutil
from core.app_paths import resource_path, data_dir

class AppController:
    def __init__(self):
        self.current_role = None
        self.main_window = None
        self.login_window = None

    def show_login(self):
        """Відображає вікно входу"""
        self.login_window = LoginWindow(self) 
        self.login_window.show()

    def show_main_window(self):
        """Відображає головне вікно після авторизації"""
        self.main_window = MainWindow(self.current_role, self) 
        self.main_window.show()

    def logout(self):
        """Закриває головне вікно та повертає до авторизації"""
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        self.current_role = None
        self.show_login() 

def init_database_if_needed():
    src_db = resource_path("database")
    dst_db = data_dir()
    marker = dst_db / "users.txt"
    if marker.exists():
        return
    shutil.copytree(src_db, dst_db, dirs_exist_ok=True)

def main():
    app = QApplication(sys.argv)
    init_database_if_needed()
    
    style_path = resource_path("assets/style.qss")
    if style_path.exists():
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    controller = AppController()
    controller.show_login()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()