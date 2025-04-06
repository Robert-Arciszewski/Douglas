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

# Katalog, w którym mają być zapisane katalogi brandów
output_dir = "brands_output"
os.makedirs(output_dir, exist_ok=True)

# Zbiór danych do zapisu: słownik {brand: [product_ids]}
brand_product_map = defaultdict(list)

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

        # Dodajemy ID produktu do listy dla danej marki
        brand_product_map[brand].append(product_id)

# Tworzenie katalogów i zapisywanie plików tekstowych
for brand, product_ids in brand_product_map.items():
    # Sanityzacja nazwy marki, aby nie zawierała niedozwolonych znaków
    sanitized_brand = sanitize_filename(brand)

    # Tworzymy katalog dla marki
    brand_dir = os.path.join(output_dir, sanitized_brand)
    os.makedirs(brand_dir, exist_ok=True)

    # Tworzymy plik tekstowy o nazwie marki
    brand_file_path = os.path.join(brand_dir, f"{sanitized_brand}.txt")
    with open(brand_file_path, 'w', encoding='utf-8') as brand_file:
        # Zapisujemy ID produktów w formacie "id", "id"
        brand_file.write(", ".join([f'"{product_id}"' for product_id in product_ids]))

    print(f"✅ Utworzono plik dla {sanitized_brand} z {len(product_ids)} ID")
