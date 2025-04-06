from playwright.sync_api import sync_playwright
import csv
import time

def scrape_brands():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Możesz zmienić na True, jeśli nie chcesz widzieć okna
        context = browser.new_context()
        page = context.new_page()

        print("Wchodzę na stronę...")
        page.goto("https://www.douglas.pl/pl/brands", timeout=60000)
        time.sleep(5)  # Czekamy na załadowanie wszystkiego

        # Scrollujemy, by załadować wszystkie marki
        page.evaluate("""() => { window.scrollBy(0, document.body.scrollHeight); }""")
        time.sleep(3)

        # Pobieramy wszystkie marki i linki
        brand_elements = page.query_selector_all("a.brand-overview-page__section-link")

        brands = []
        for brand in brand_elements:
            name_span = brand.query_selector("span.brand-overview-page__section-link-brand")
            if name_span:
                brand_name = name_span.inner_text().strip()
                href = brand.get_attribute("href").strip()
                # Wyciągamy tylko końcowy fragment, np. b2903
                brand_code = href.split("/")[-1] if href else ""
                brands.append({
                    "Brand": brand_name,
                    "URL": f"https://www.douglas.pl{href}",
                    "Brand_URL_Part": brand_code
                })

        print(f"Znaleziono {len(brands)} marek.")

        # Zapisujemy do CSV
        with open("brands_all.csv", mode="w", newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["Brand", "URL", "Brand_URL_Part"])
            writer.writeheader()
            writer.writerows(brands)

        print("Zapisano do brands_all.csv")
        browser.close()

if __name__ == "__main__":
    scrape_brands()
