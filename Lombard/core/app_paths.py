from pathlib import Path
import sys


def resource_path(relative_path: str) -> Path:
    """
    Ресурси (assets, dll, початкова database):
    - exe → всередині _MEIPASS
    - python → від кореня проєкту
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parents[1] / relative_path


def data_dir() -> Path:
    """
    Постійні дані користувача:
    Documents/LombardData
    """
    base = Path.home() / "Documents" / "LombardData"
    base.mkdir(parents=True, exist_ok=True)
    return base


def data_file(filename: str) -> Path:
    """
    Конкретний файл у LombardData
    """
    return data_dir() / filename
