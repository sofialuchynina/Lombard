import os
import sys
import ctypes
from core.app_paths import data_file, resource_path

DLL_PATH = str(resource_path(os.path.join("boss", "boss.dll")))

def get_boss_lib():
    """Завантажує C++ бібліотеку та налаштовує типи даних."""
    if not os.path.exists(DLL_PATH):
        raise FileNotFoundError(f"C++ бібліотеку не знайдено за шляхом: {DLL_PATH}")

    lib = ctypes.CDLL(DLL_PATH)

    lib.boss_items_statistics.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    lib.boss_items_statistics.restype = ctypes.c_int

    lib.boss_detect_anomalies.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double]
    lib.boss_detect_anomalies.restype = ctypes.c_int

    lib.boss_sort_items.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    lib.boss_sort_items.restype = ctypes.c_int
    
    return lib

def build_statistics():
    """Викликає C++ для збору статистики (звіт у director_stat.txt)."""
    items_path = str(data_file("items.txt").resolve())
    out_path = str(data_file("director_stat.txt").resolve())
    
    try:
        lib = get_boss_lib()
        result = lib.boss_items_statistics(items_path.encode('utf-8'), out_path.encode('utf-8'))
        return result == 0
    except Exception as e:
        print(f"Помилка при запуску C++ статистики: {e}")
        return False

def detect_anomalies(factor=1.5):
    """Викликає C++ для виявлення аномалій (звіт у anomalies.txt)."""
    items_path = str(data_file("items.txt").resolve())
    out_path = str(data_file("anomalies.txt").resolve())
    try:
        lib = get_boss_lib()
        result = lib.boss_detect_anomalies(
            items_path.encode('utf-8'), 
            out_path.encode('utf-8'), 
            float(factor)
        )
        return result == 0
    except Exception as e:
        print(f"Помилка при пошуку аномалій: {e}")
        return False

def sort_items_by_price(ascending=True):
    """Викликає C++ для сортування (звіт у sorted_items.txt)."""
    items_path = str(data_file("items.txt").resolve())
    out_path = str(data_file("sorted_items.txt").resolve())
    try:
        lib = get_boss_lib()
        result = lib.boss_sort_items(
            items_path.encode('utf-8'), 
            out_path.encode('utf-8'), 
            1 if ascending else 0
        )
        return result == 0
    except Exception as e:
        print(f"Помилка при сортуванні: {e}")
        return False