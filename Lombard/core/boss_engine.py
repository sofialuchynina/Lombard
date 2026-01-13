import os
from core.app_paths import data_file

def build_statistics():
    items_path = data_file("items.txt")
    out_path = data_file("director_stat.txt")

    stats = {
        "total": 0,
        "available": 0,
        "sold": 0,
        "pawn": 0,
        "returned": 0,
        "total_value": 0.0
    }

    if items_path.exists():
        with open(items_path, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
            content = lines[1:] if len(lines) > 1 else []
            
            for line in content:
                parts = line.strip().split("|")
                if len(parts) < 4:
                    continue

                try:
                    price_val = float(parts[2].replace("-0", "").strip())
                except ValueError:
                    price_val = 0.0
                
                status = parts[3].strip().lower()

                stats["total"] += 1
                stats["total_value"] += price_val

                if status == "в наявності":
                    stats["available"] += 1
                elif status == "продано":
                    stats["sold"] += 1
                elif status == "застава":
                    stats["pawn"] += 1
                elif status == "повернено клієнту":
                    stats["returned"] += 1

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"total={stats['total']}\n")
        f.write(f"available={stats['available']}\n")
        f.write(f"sold={stats['sold']}\n")
        f.write(f"pawn={stats['pawn']}\n")
        f.write(f"returned={stats['returned']}\n")
        f.write(f"total_value={int(stats['total_value'])}\n")