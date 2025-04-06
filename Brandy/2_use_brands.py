import csv
import os
from collections import defaultdict
import re

# Funkcja do czyszczenia nazw katalogów (usuwa niedozwolone znaki)
def sanitize_filename(filename):
    # Usuwamy znaki niedozwolone w Windows
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Ścieżka do pliku CSV
csv_filename = "all_products.csv"

# Katalog, w którym mają być zapisane pliki
output_dir = "brands_output"
os.makedirs(output_dir, exist_ok=True)

# Zbiór danych do zapisu: lista wszystkich ID
all_product_ids = []

# Otwórz i odczytaj plik CSV
with open(csv_filename, newline='', encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file)

    # Pomijamy nagłówek
    next(reader)

    for row in reader:
        # Upewnij się, że wiersz ma dokładnie 3 elementy
        if len(row) != 3:
            continue  # Pomijamy wiersze, które nie mają trzech elementów

        brand, product_url, product_info = row

        # Wyciągamy ID produktu z URL
        product_id = product_url.split('/')[-1].split('?')[0]

        # Dodajemy ID produktu do ogólnej listy
        all_product_ids.append(product_id)

# Tworzenie pliku, w którym zapisujemy wszystkie ID w grupach po 1000
output_file = os.path.join(output_dir, "all_product_ids.txt")

# Tworzymy plik, który zawiera wszystkie ID w formacie "id", "id" w jednym pliku
with open(output_file, 'w', encoding='utf-8') as output_file_txt:
    chunk_size = 1000
    for i in range(0, len(all_product_ids), chunk_size):
        chunk = all_product_ids[i:i + chunk_size]
        # Zapisujemy ID produktów w formacie "id", "id", każda grupa w jednej linii
        output_file_txt.write(", ".join([f'"{product_id}"' for product_id in chunk]) + "\n")

    print(f"✅ Utworzono plik {output_file} z wszystkimi ID")
