import sys
import shutil
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from gui.login_window import LoginWindow
from gui.main_window import MainWindow
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
        if self.login_window:
            self.login_window.close()
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
    """
    Гарантує, що база даних існує в Documents/LombardData.
    Це критично для роботи C++ DLL в режимі EXE.
    """
    src_db = resource_path("database")
    dst_db = data_dir() # Шлях до Documents/LombardData
    
    # Перевіряємо наявність основних файлів
    marker = dst_db / "users.txt"
    items_file = dst_db / "items.txt"
    
    try:
        if not marker.exists() or not items_file.exists():
            if src_db.exists():
                # Копіюємо початкові файли з ресурсів EXE у Документи
                shutil.copytree(src_db, dst_db, dirs_exist_ok=True)
                print(f"Дані ініціалізовано у: {dst_db}")
            else:
                print("Помилка: Початкова база даних не знайдена в ресурсах.")
    except Exception as e:
        print(f"Критична помилка ініціалізації даних: {e}")

def check_cpp_dependencies():
    """Перевірка наявності DLL перед запуском"""
    dll_path = resource_path(os.path.join("boss", "boss.dll"))
    if not dll_path.exists():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Критична помилка системи!")
        msg.setInformativeText(f"C++ бібліотека (boss.dll) не знайдена.\nШлях: {dll_path}")
        msg.setWindowTitle("Помилка запуску")
        msg.exec_()
        return False
    return True

def main():
    app = QApplication(sys.argv)
    
    # 1. Підготовка даних та перевірка ресурсів
    init_database_if_needed()
    if not check_cpp_dependencies():
        sys.exit(1)
    
    # 2. Завантаження стилів
    style_path = resource_path("assets/style.qss")
    if style_path.exists():
        try:
            with open(style_path, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Не вдалося завантажити стилі: {e}")

    # 3. Запуск контролера
    controller = AppController()
    controller.show_login()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()