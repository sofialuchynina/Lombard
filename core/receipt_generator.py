import pdfkit
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from core.app_paths import data_file
import os

def generate_receipt(operation, item_name, amount, client_name=None):

    path = data_file("recipes.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n========================================\n")
        f.write("ЛОМБАРД — КВИТАНЦІЯ\n")
        f.write("----------------------------------------\n")
        f.write(f"Дата: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
        f.write(f"Клієнт: {client_name or 'Невідомий'}\n")
        f.write(f"Операція: {operation}\n")
        f.write(f"Товар: {item_name}\n")
        f.write(f"Сума: {amount} грн\n")
        f.write("----------------------------------------\n")
        f.write("Підпис працівника: ____________\n")
        f.write("========================================\n")
    return str(path)

def export_to_pdf(receipt_data, output_path):

    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    
    if not os.path.exists(path_wkhtmltopdf):
        raise FileNotFoundError(f"wkhtmltopdf не знайдено за шляхом: {path_wkhtmltopdf}")

    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    assets_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')

    env = Environment(loader=FileSystemLoader(assets_dir))
    template = env.get_template('pdf_template.html')

    html_content = template.render(receipt_data)

    options = {
        'page-size': 'A5',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': "UTF-8",
        'quiet': '',
        'enable-local-file-access': None
    }

    pdfkit.from_string(html_content, output_path, options=options, configuration=config)