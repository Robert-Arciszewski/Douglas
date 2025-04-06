from playwright.sync_api import sync_playwright
import csv
import time

def scrape_douglas_products(brand_url_part, brand_name):
    base_url = f"https://www.douglas.pl/pl/b/{brand_url_part}"
    output_file = f"{brand_name}_products.csv"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # True = bez okna
        context = browser.new_context()
        page = context.new_page()

        print(f"Otwieranie strony: {base_url}")
        page.goto(base_url, timeout=60000)
        time.sleep(5)

        # Scrollowanie by doładować produkty
        print("Scrollowanie strony...")
        previous_height = 0
        while True:
            page.mouse.wheel(0, 5000)
            time.sleep(2)
            current_height = page.evaluate("document.body.scrollHeight")
            if current_height == previous_height:
                break
            previous_height = current_height

        print("Zbieranie produktów...")

        # Zbieramy produkty
        product_elements = page.query_selector_all("a[data-testid='details-link']")
        products = []
        for product in product_elements:
            product_url = product.get_attribute("href")
            product_info = product.inner_text().replace("\n", " | ").strip()
            products.append({
                "Product URL": f"https://www.douglas.pl{product_url}",
                "Product Info": product_info
            })

        # Zapis do CSV
        csv_filename = f"{brand_name}_products.csv"
        with open(csv_filename, mode="w", newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["Product URL", "Product Info"])
            writer.writeheader()
            writer.writerows(products)

        print(f"Pobrano {len(products)} produktów dla marki {brand_name}. Zapisano do pliku {csv_filename}")

        browser.close()

# Użycie przykładowe
scrape_douglas_products("100bon/b5914", "100BON")
