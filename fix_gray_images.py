import csv

input_csv = "1_douglas_product_full.csv"
output_csv = "1_douglas_product_fixed.csv"

with open(input_csv, newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames.copy()

    # Upewnij się, że kolumna z szarym zdjęciem istnieje
    if "Main Image (Gray)" not in fieldnames:
        fieldnames.append("Main Image (Gray)")

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        main_img = row.get("Main Image", "").strip()
        gray_img = row.get("Main Image (Gray)", "").strip()

        if main_img and not gray_img:
            row["Main Image (Gray)"] = f"{main_img}&grid=true&imPolicy=grayScaled"

        writer.writerow(row)

print("✅ Naprawiono plik CSV. Zapisano jako:", output_csv)
