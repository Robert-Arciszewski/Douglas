import xml.etree.ElementTree as ET
import csv

input_file = "produkty3.xml"
output_file = "produkty3.csv"

tree = ET.parse(input_file)
root = tree.getroot()

fieldnames = [
    "id", "sku", "name", "description", "url", "image", "weight",
    "category", "producer", "ean", "code",
    "price_netto", "VAT", "qty"
]

def get_property(offer, key):
    for prop in offer.findall("property"):
        if prop.get("name") == key:
            return (prop.text or "").strip()
    return ""

with open(output_file, mode="w", newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for offer in root.findall("offer"):
        row = {
            "id": offer.findtext("id", "").strip(),
            "sku": offer.findtext("sku", "").strip(),
            "name": offer.findtext("name", "").strip(),
            "description": offer.findtext("description", "").strip(),
            "url": offer.findtext("url", "").strip(),
            "image": offer.find("images/image").text.strip() if offer.find("images/image") is not None else "",
            "weight": offer.findtext("weight", "").strip(),
            "category": offer.findtext("category", "").strip(),
            "producer": offer.findtext("producer", "").strip(),
            "ean": get_property(offer, "ean"),
            "code": get_property(offer, "code"),
            "price_netto": get_property(offer, "price_netto"),
            "VAT": get_property(offer, "VAT"),
            "qty": offer.findtext("qty", "").strip()
        }
        writer.writerow(row)

print(f"✔️ Zapisano {output_file}")