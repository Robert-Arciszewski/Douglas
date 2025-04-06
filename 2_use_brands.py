from playwright.sync_api import sync_playwright
import csv
import time

HEADLESS = False  # True = w tle, False = widoczne okno

def accept_cookies(page):
    try:
        page.wait_for_selector("button[data-testid='uc-accept-all-button']", timeout=5000)
        page.click("button[data-testid='uc-accept-all-button']")
        print("Kliknięto Akceptuję cookies.")
        time.sleep(1)
    except:
        print("Brak popup cookies lub już kliknięto.")

def scroll_page(page, brand_name):
    print(f"Scrollowanie dla marki {brand_name}...")
    previous_height = 0
    retries = 0
    while True:
        page.mouse.wheel(0, 5000)
        time.sleep(1.5)
        current_height = page.evaluate("document.body.scrollHeight")
        if current_height == previous_height:
            retries += 1
            if retries >= 3:
                break
        else:
            retries = 0
        previous_height = current_height
    print("Scrollowanie zakończone.")

def scrape_douglas_products(page, brand_url_part, brand_name, writer):
    base_url = f"https://www.douglas.pl/pl/b/{brand_url_part}"

    print(f"Otwieranie strony: {base_url}")
    try:
        page.goto(base_url, timeout=60000)
        time.sleep(3)
        accept_cookies(page)
    except Exception as e:
        print(f"Błąd otwierania strony {brand_name}: {e}")
        return

    scroll_page(page, brand_name)

    print(f"Zbieranie produktów dla marki {brand_name}...")

    product_elements = page.query_selector_all("a[data-testid='details-link']")
    products = []
    for product in product_elements:
        product_url = product.get_attribute("href")
        product_info = product.inner_text().replace("\n", " | ").strip()
        products.append({
            "Brand": brand_name,
            "Product URL": f"https://www.douglas.pl{product_url}",
            "Product Info": product_info
        })

    print(f"Pobrano {len(products)} produktów dla marki {brand_name}.")

    for p in products:
        writer.writerow(p)

def main():
    brands = []
    with open("brands_all.csv", mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            brands.append({
                "Brand": row["Brand"],
                "Brand_URL_Part": row["Brand_URL_Part"]
            })

    print(f"Wczytano {len(brands)} marek do przetworzenia.")

    output_file = "all_products_lapreirie_plus.csv"
    with open(output_file, mode="w", newline='', encoding='utf-8') as csv_out:
        fieldnames = ["Brand", "Product URL", "Product Info"]
        writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
        writer.writeheader()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS)

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 800},
                locale='pl-PL'
            )

            # STEALTH
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                window.navigator.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'languages', { get: () => ['pl-PL', 'pl'] });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            """)

            page = context.new_page()

            # Główna strona, cookies
            try:
                page.goto("https://www.douglas.pl", timeout=60000)
                accept_cookies(page)
            except Exception as e:
                print(f"Błąd przy otwieraniu głównej strony: {e}")

            # Lecimy po markach
            for idx, brand in enumerate(brands, 1):
                print(f"\n[{idx}/{len(brands)}] Przetwarzam markę: {brand['Brand']}")
                scrape_douglas_products(page, brand["Brand_URL_Part"], brand["Brand"], writer)
                time.sleep(2)

            browser.close()

    print(f"\nZakończono! Wszystkie produkty zapisane w {output_file}")

if __name__ == "__main__":
    main()
