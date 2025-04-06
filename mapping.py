import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# === 1. Wczytanie plików Excel ===
douglas_df = pd.read_excel("D_26/26_douglas.xlsx")
htg_df = pd.read_excel("HTG_STOCK_ALL.xlsx")

# === 2. Czyszczenie potencjalnych NaN ===
douglas_df["Product Name"] = douglas_df["Product Name"].fillna("")
htg_df["Name"] = htg_df["Name"].fillna("")

# === 3. Funkcja dopasowania fuzzy z zabezpieczeniem ===
def find_best_match(product_name, choices, threshold=85):
    if not isinstance(product_name, str) or not product_name.strip():
        return None
    result = process.extractOne(product_name, choices, scorer=fuzz.token_sort_ratio)
    if result:
        best_match = result[0]
        score = result[1]
        if score >= threshold:
            return best_match
    return None

# === 4. Dopasowywanie nazw ===
matched_names = []
matched_skus = []
matched_eans = []

for name in douglas_df["Product Name"]:
    match = find_best_match(name, htg_df["Name"])
    if match:
        row = htg_df[htg_df["Name"] == match].iloc[0]
        matched_names.append(match)
        matched_skus.append(row.get("SKU", ""))
        matched_eans.append(row.get("EAN Barcode", ""))
    else:
        matched_names.append("")
        matched_skus.append("")
        matched_eans.append("")

# === 5. Dodanie kolumn z wynikami ===
douglas_df["Matched Name"] = matched_names
douglas_df["SKU"] = matched_skus
douglas_df["EAN"] = matched_eans

# === 6. Eksport wyników ===
output_filename = "D_26/26_douglas_big.xlsx"
douglas_df.to_excel(output_filename, index=False)

print(f"✅ Zapisano plik: {output_filename}")
