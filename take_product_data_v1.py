import requests
import csv
import json

# Produkt ID
product_id = "5010936003"

# URL API
url = f"https://www.douglas.pl/api/v2/products/{product_id}?fields=FULL"
headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Pobieranie danych
response = requests.get(url, headers=headers)
print("Status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))

if response.status_code == 200 and "application/json" in response.headers.get("Content-Type"):
    product_data = response.json()

    # 🔹 Zapis surowego JSON-a do pliku .txt
    with open("douglas_product_raw.txt", mode="w", encoding="utf-8") as raw_file:
        raw_file.write(json.dumps(product_data, indent=2, ensure_ascii=False))
    print("Zapisano cały JSON do douglas_product_raw.txt")

    # 🔹 Wyciąganie danych uproszczonych
    simplified_data = {
        "Product ID": product_data.get("code", ""),
        "Product Name": product_data.get("name", ""),
        "Brand": product_data.get("brand", {}).get("name", ""),
        "Brand Code": product_data.get("brand", {}).get("code", ""),
        "EAN": product_data.get("ean", ""),
        "Price": product_data.get("price", {}).get("formattedValue", ""),
        "Currency": product_data.get("price", {}).get("currencyIso", ""),
        "Stock Status": product_data.get("stock", {}).get("stockLevelStatus", ""),
        "Availability": product_data.get("availability", {}).get("message", ""),
        "Average Rating": product_data.get("averageRating", 0.0),
        "Number of Reviews": product_data.get("numberOfReviews", 0),
        "Categories": " | ".join([cat['name'] for cat in product_data.get("categories", [])]),
        "Bullet Points": " | ".join(product_data.get("bulletPoints", [])),
        "Description (HTML)": product_data.get("description", ""),
        "Images": " | ".join([img['url'] for img in product_data.get("images", [])]),
        "Product URL": f"https://www.douglas.pl{product_data.get('baseProductUrl', '')}",
        "Volume Info": f"{product_data.get('baseNumberContentUnits', '')} {product_data.get('contentUnit', '')}",
        "Lowest Price Info": product_data.get("lowestPriceBeforePromotion", {}).get("formattedValue", ""),
        "Product Type": product_data.get("productType", ""),
        "Is Medicine": product_data.get("isMedicine", False),
        "Is RX": product_data.get("isRX", False),
    }

    # 🔹 Zapis uproszczonych danych do CSV
    with open("douglas_product_full.csv", mode="w", newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=simplified_data.keys())
        writer.writeheader()
        writer.writerow(simplified_data)

    print("Dane zapisane do douglas_product_full.csv")

else:
    print("Błąd pobierania danych lub nieprawidłowy format.")
