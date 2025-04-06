import os
import csv
import json
import re
import requests
from pathlib import Path

def slugify(text: str, max_length=100) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")[:max_length]

def download_image(url: str, path: Path):
    if not url:
        return ""
    try:
        img_data = requests.get(url).content
        with open(path, 'wb') as handler:
            handler.write(img_data)
        return path.name
    except Exception as e:
        print(f"❌ Błąd pobierania zdjęcia: {url} -> {e}")
        return ""

# Konfiguracja
product_ids = [

"5011701010", "5011701009", "5011397047", "5011605001", "5010601008", "5010150043", "5010150057", "5010150044", "5010150045", "5011035026", "5011004007", "5010940010", "5010826018", "5010601009", "5010592016", "5010370026", "5010370025", "5010409002", "5010126008", "5010126004", "5010126005", "5010126003", "5010121068", "5010126010", "5010126007", "5010121055", "5010126009", "5010126006", "5010126001", "5010126002", "5010121060", "5010121057", "m000497271", "m000570006", "m000570055", "m000570053", "m000601198", "m000600017", "m000588458", "m000585001", "m000570095", "m000570092", "m000570090", "m000570086", "m000570087", "m000570084", "m000570082", "m000570080", "m000570078", "m000570077", "m000570076", "m000570058", "m000570057", "m000570054", "m000570047", "m000570045", "m000570043", "m000570042", "m000570039", "m000570035", "m000570030", "m000570029", "m000570028", "m000570026", "m000570021", "m000570018", "m000570015", "m000570014", "m000570013", "m000570012", "m000570002", "5010537125", "5010537120", "5010537110", "5010537107", "5010537111", "5010327081", "5010327069", "5010327025", "5009398033", "5009398032", "m001918036", "m002061111", "m001918054", "m002371002", "m002371001", "m002368206", "m002368207", "m002368202", "m002370022", "m002368204", "m002368203", "m002370032", "m002368185", "m002370039", "m002368187", "m002368209", "m002368180", "m002142044", "m001918025", "m002163021", "m001580362", "m002061112", "m001528134", "m002111183", "m002030007", "m000015213", "m001543005", "m001910450", "m002296096", "m002287004", "m002270062", "m002255099", "m002255066", "m002197014", "m002180005", "m002160131", "m002142046", "m002111209", "m002111193", "m002111184", "m002111182", "m002112901", "m002091002", "m002091000", "m002091001", "m002085105", "m002085102", "m002061115", "5003725154", "5011687002", "5011543089", "3001020216", "3001020232", "5010620203", "3001020311", "5011317018", "5010964033", "5011450054", "3001035189", "3001042860", "5011450050", "5011080008", "5010973103", "3001056452", "5011250016", "5011250017", "5002333013", "5010841023", "3001044328", "5002487518", "5011549086", "3001042851", "5002484396", "3001035191", "5011450053", "3001051154", "5011549081", "5010515020", "5002484394", "5010620179", "3001056449", "5011450052", "5011539333", "5011450051", "5011086000", "5010886042", "5010785095", "5010387030", "5010387028", "5010387029", "5010046008", "5010046006", "5009262033", "5009262032", "5009262031", "5009262030", "5003623017", "5009848052", "5009848005", "5009848001", "5011451092", "5011463242", "5011463240", "5011602008", "5011656142", "5011463238", "5011656144", "5011656147", "5011656145", "5011489063", "5011489064", "5011489062", "5011656143", "5011489052", "5011463237", "5011656146", "5011489050", "5011489051", "5011489068", "5011658025", "5011583027", "5011489067", "5011489066", "5011489061", "5011489048", "5011489049", "5010468116", "5010399037", "5010393043", "5010393042", "5010393039", "5010393040", "5010393038", "5010393033", "5010393032", "5010393031", "5010393029", "5010393027", "5011463236", "5011463239", "5011463235", "5011489059", "5011489065", "5011489053", "5010399036", "5010399034", "5010399035", "5011425008", "5011639008", "m001500022", "m001500025", "5011639010", "m001529011", "m001529038", "5011639004", "5011639009", "5011639011", "m001529024", "m001529054", "m001529057", "m001529023", "5011639013", "5011639012", "m001529063", "m001529056", "m001529021", "m001529018", "m001529007", "m001529020", "m001531003", "5011076011", "5011076015", "5011076006", "5011076014", "5011076010", "5011076016", "5011076007", "5011076008", "5011076012", "5010868171", "5001775003", "5010934006", "5011043000", "5009765073", "5001771006", "5010868173", "5011070006", "5001771007", "5010868167", "5011114007", "5010643091", "5010643085", "5010533008", "5011092046", "5010238006", "5010868170", "5010533013", "5010805121", "5011551027", "5010868169", "5010934004", "5010805109", "5010533012", "5010533014", "5001774001", "5011071026", "5010643086", "5010643087", "5010643093", "5009765088", "5010533017", "5011284626", "m000480334", "5010805108", "5010238005", "5011284039", "5011045002", "5001773022", "5011114006", "5010567140", "5010238004", "5010643089", "5011551026", "5010934007", "5010453039", "5010598076", "5011114004", "3000071837", "3000071817", "3000071808", "3000071814", "3000071805", "3000071804", "3000071824", "3000071828", "3000071845", "3000071823", "3000071778", "5011499021", "5009038023", "5009038026", "5010033066", "5009039007", "5009038021", "5009038020", "5009038022", "5009039009", "5009038034", "5010036002", "5009001008", "5009001013", "5010134069", "5009008028", "5009038008", "5010036001", "5009038007", "5009038025", "5010036003", "5010136014", "5010036000", "5009038010", "5009038004", "5009038031", "5009003000", "5009001009", "5009001007", "5009001006", "5009752152", "5009752155", "5009752156", "5010377047", "5010967003", "5011359011", "5011099015", "5011099012", "5011359013", "5011036061", "5011359014", "5010334025", "5011251018", "5011099013", "5011251017", "5002458029", "5010824150", "5010824149", "5011397047", "5010756041", "3001044289", "5011359012", "3001055719", "5010756040", "5011461037", "5010918017", "5010756042", "5010641003", "5010466001", "5001764651", "5011469042", "5002312002", "5011183026", "5009765106", "5011183025", "5010974114", "5010979079", "5009897002", "5010334072", "5010026035", "5010974112", "3001024525", "5010641000", "3001050625", "m000249439", "5011129011", "5011036062", "5010756039", "5010791164", "5010967001", "5001017064", "5010974120", "m001206653", "m002258148", "m001694259", "m002155106", "m002111206", "m002040031", "m001979023", "m001979026", "m001974032", "m001948044", "m001856138", "m001559028", "m001847120", "m001847049", "m001694250", "m001600324", "m001539066", "m001206283", "m000974899", "m000459212", "m000231346", "m000015031", "m000014559", "5010534053", "m000968164", "m000968285", "3001024067", "3001024069", "5002053011", "5002053008", "5001914041", "3001024064", "3001024066", "3001024065", "5002054025", "3001024070", "5009143014", "5009143018", "5009143016", "5009143015", "5009143011", "5009143005", "5010319100", "5010319101", "5010737146", "5010863004", "5010737144", "5002492205", "5002492175", "5002492206", "5002492179", "5010517066", "5010517070", "5009144049", "5010517067", "5010517078", "5009144050", "5009144046", "5009144042", "5009144039", "5009144030", "5009144027", "5009144025", "5009144037", "5009144029", "5009144017", "5010517076", "5010517077", "5009144022", "5010517072", "5010517071", "5010517068", "5010517074", "5009950037", "5009144051", "5009144048", "5009144047", "5009144028", "5009144014", "5009144013", "5009144023", "5011129010", "5009883030", "5009974006", "5010468166", "5009974007", "5009883028", "5009974008", "5011129009", "5011006261", "5010834054", "5009883031", "5010871015", "5010855040", "5009883029", "5009974005", "5009974009", "5010662060", "5010662056", "m000457226", "m002004030", "5010666016", "5010666018", "5010635036", "m001049164", "m000457303", "m000457139", "m000457029", "3001003153", "3000000320", "3000000317", "3000056016", "m000169005", "m000106323", "m000169006", "m000422185", "m000422093", "m000422418", "m000418084", "m000418100", "m000418076", "m000418028", "m000376515", "m000376402", "m000168248", "m000168262", "m000168074", "m000168251", "m000169003", "m000168250", "m000168247", "m000168252", "m000106304", "m000166466", "m000171655", "m000168065", "m000169002", "m000166465", "m000168012", "m000168259", "m000169000", "m000106215", "m000168260", "m000168039", "m000171548", "m000106089", "m000168033", "m000106072", "m000168053", "m000106053", "m000168007", "m000106015", "m000106014", "m000168057", "m002039150", "m002254095", "m002251018", "m002041076", "5011301017", "m002254073", "5011657017", "m002258381", "m002254045", "5011601055", "5011522102", "5011522101", "5011371001", "5010686122", "5010686111", "5010686115", "5010686092", "5010686093", "5003222091", "5003222105", "5011734046", "5011734047", "5011734048", "5011734042", "5010547001", "5003222109", "5010544317", "5010547000", "5009227029", "5003222099", "5010547032", "5010547026", "5009227033", "5009227030", "5010544314", "5009227036", "5009227057", "5010508162", "5003222100", "5010508163", "5010544316", "5010547022", "5010547010", "5010547003", "5009227031", "3001007442", "3001013165", "5003076083", "5003076079", "5003076075", "5003076071", "5010539082", "5010539081", "5010539077", "5010539085", "5010539088", "5010539083", "5010539090", "5010539092", "5010539086", "5010539079", "5010539089", "5010539073", "5010539087", "5010505143", "5010539078", "5010539084", "5010539091", "5010539080", "5010505226", "5010505154", "5010539075", "5009939243", "5009939235", "5009939249", "5009939215", "5009939224", "5009939238", "5009939212", "5009939259", "5009939227", "5009939242", "5009939252", "5009939256", "5009939231", "5003701014", "3000046360", "1008601304", "5011077064", "5011077062", "5011077079", "5011077074", "5011077075", "5011077072", "5011077070", "5011077069", "5011077066", "5011077067", "5011077063", "5011077058", "5011077073", "5011077076", "5011077065", "m001855007", "m001197067", "m002110182", "m002110174", "m002111188", "m002111170", "m002110162", "m002145065", "m002112936", "m002110092", "m002112904", "m002112899", "m002112890", "5011613008", "5011582040", "m001231097", "5011613009", "5011613007", "5011604059", "5011582038", "5011582041", "5011582037", "5011582039", "5011545315", "5011545314", "5011545310", "5011545166", "5011530119", "5011530118", "5011530113", "5011530110", "5011530114", "5011530111", "m002055025", "5010903116", "5010903118", "5010903117", "5010519591", "5010519582", "5010173012", "5010173002", "5010029095", "5010029096", "5010029097", "5010029100", "5010029074", "5010029072", "5010029065", "5010029090", "5010029067", "5010029094", "5010029079", "5010029099", "5010865134", "5010865170", "5010865150", "5011457023", "5011457041", "5011457040", "5010865152", "5010865137", "5010865145", "5010865114", "5011457013", "5010865156", "5011457024", "5010865113", "5010865169", "5010865162", "5010865160", "5011457036", "5010865110", "5010865126", "5010865118", "5010865117", "5010865172", "5010865165", "5010865167", "5010865168", "5010865161", "5011457015", "5010865171", "5010865116", "5011457037", "5011457025", "5011457038", "5010865141", "5010865155", "5010865149", "5010865148", "5010865140", "5011036021", "5010865147", "5010865146", "5010865143", "5010865130", "5010865154", "5010865159", "5011457039", "5010865157", "5010865136", "5009507016", "5009507020", "5002489850", "5009507017", "1010401304", "5010693069", "5010693088", "5010693087", "5010693103", "5010693065", "5010693074", "5010693061", "5010693083", "5010693101", "5010693066", "5010693057", "5010693073", "5010693064", "5010693107", "5010693067", "5010693085", "5010693086", "5010693080", "5010693104", "5010693081", "5010693100", "5010693063", "5010693060", "5010693102", "5010693105", "5010693059", "5010693068", "5010693058", "5010693084", "5010693098", "5010693070", "5010693062", "5010693072", "5010693082", "5010693079", "5000191064", "5010343006", "5010696094", "5011367006", "5000191065", "5010740022", "5010343007", "3001049025", "5010546099", "3001049024", "5010350078", "5010546105", "5010546104", "5010546103", "5010546102", "5010546101", "5010546100", "5011376046", "3001047505", "5010255114", "5011503067", "3001020196", "5010463028", "5002225041", "5011286192", "5011683002", "5011023033", "5010692000", "5010887041", "3001042355", "5011238003", "5001543080", "5010459064", "2001004557", "5010865232", "1013620304", "5010900083", "5011582160", "5011563066", "5009994000", "5011574263", "1013601304", "5002558000", "5011574262", "5009752136", "5011570012", "5011588142", "5011407392", "3001038061", "5011655023", "5011563070", "5011407390", "5010681033", "5011407394", "5010882006", "5010655001", "1013612304", "5010653122", "5010904024", "5010508236", "1013617295", "3001047507", "m000075002", "m000075006", "3001050582", "3001050583", "5010515021", "5010468096", "5010468093", "5010468099", "5010468084", "5010960622", "5010468069", "5010468076", "5011316015", "5010468101", "5010468083", "5011316021", "5010468102", "5010503015", "5010468094", "5011316016", "5010468086", "5011316017", "5010468072", "5010468071", "5010468095", "5010468091", "5010468070", "5011316019", "5011316018", "5011316023", "5011316025", "5010468078", "5010468080", "5010468081", "5011316024", "5010468092", "5010468087", "5011316013", "5010468088", "5010468068", "5010468082", "5010468100", "5010468097", "5010468090", "5010468074", "5011316014", "5011316020", "5010468110", "5011316022", "5010468085", "5010468073", "m002379036", "m000451023", "m000915062", "m002396000", "m002379024", "m002379065", "m002379023", "m002379050", "m002379059", "m002379004", "m002379001", "m002379020", "m002379017", "m002379022", "m002379053", "m002379003", "m002379041", "m002379070", "m002379047", "m002379048", "m002375096", "m002376099", "m002375061", "m002376103", "m002375087", "m002375084", "m002376108", "m002375128", "m002375090", "m002376109", "m002371127", "m002371125", "m002371128", "m002327021", "m002329015", "m002327026", "m002329003", "m002327022", "m002327023", "m002329002", "m002329011", "m002329005", "m002329001", "m002327024", "m002329013", "m002329008", "m002329010", "m002329009", "5009978053", "5009978051", "5009978060", "5009978037", "5009978019", "5009978055", "5010207044", "5009978043", "5009978033", "5009978005", "5010516015", "5009975096", "5009975083", "5010516014", "5009978027", "5009978044", "5009975103", "5009975092", "5009975090", "5009583007", "5010825106", "5010432222", "5010434070", "5003425091", "5010044063", "5010003182", "5010848040", "5010848037", "5011068011", "5009401047", "5010848038", "5010845109", "5010813025", "5010845118", "5010845108", "5010813037", "5003425092", "m002176136", "5009008004", "5010825098", "5011055000"


]  # skrócona lista do testu

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

csv_filename = "8_douglas_product_full.csv"
images_root_dir = Path("images8")
images_root_dir.mkdir(exist_ok=True)
raw_dir = Path("raw_responses")
raw_dir.mkdir(exist_ok=True)

fieldnames = [
    "Brand", "Product Name", "Product Family", "Variant Name", "Price", "Volume",
    "Description", "Application", "Ingredients", "Warnings", "Bullet Points",
    "Breadcrumbs", "Variant Image (Preview)", "Main Image", "Main Image (Gray)", "All Images",
    "Manufacturer Info"
]

file_exists = os.path.isfile(csv_filename)
write_header = not file_exists or os.path.getsize(csv_filename) == 0

with open(csv_filename, "a", newline='', encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    if write_header:
        writer.writeheader()

    for product_id in product_ids:
        url = f"https://www.douglas.pl/api/v2/products/{product_id}?fields=FULL"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print(f"❌ Błąd przy ID: {product_id} – {e}")
            continue

        raw_file_path = raw_dir / f"{product_id}_raw.json"
        with open(raw_file_path, "w", encoding="utf-8") as raw_file:
            raw_file.write(response.text)

        if "application/json" in response.headers.get("Content-Type", ""):
            product_data = response.json()
            variants = product_data.get("variantOptions", [])
            brand = product_data.get("brand", {}).get("name", "")
            brand_line = product_data.get("brandLine", {}).get("name", "")
            base_name = product_data.get("baseProductName", "")

            categories = product_data.get("categories", [])
            breadcrumb_str = " > ".join(f'{c.get("name", "")} ({c.get("url", "")})' for c in categories)

            brand_dir = images_root_dir / slugify(brand)
            brand_dir.mkdir(parents=True, exist_ok=True)

            for variant in variants:
                variant_name = variant.get("variantName", "")
                full_variant_name = f"{brand_line} {base_name} {variant_name}".strip()
                variant_slug = slugify(full_variant_name)

                variant_dir = brand_dir / variant_slug
                variant_dir.mkdir(parents=True, exist_ok=True)

                swatch_url = variant.get("previewImage", {}).get("url", "")
                swatch_path = variant_dir / f"{variant_slug}_swatch.jpg"
                swatch_file_name = download_image(swatch_url, swatch_path)

                images = variant.get("images", [])
                image_urls = []
                image_file_names = []

                # Główne zdjęcie kolorowe
                if images:
                    main_url = images[0]["url"]
                    main_path = variant_dir / f"{variant_slug}_0.jpg"
                    main_file = download_image(main_url, main_path)
                    image_urls.append(main_url)
                    image_file_names.append(main_file)

                    # Szare zdjęcie jako 1
                    gray_url = f"{main_url}&grid=true&imPolicy=grayScaled"
                    gray_path = variant_dir / f"{variant_slug}_1.jpg"
                    gray_file = download_image(gray_url, gray_path)
                    image_urls.append(gray_url)
                    image_file_names.append(gray_file)

                    # Pozostałe zdjęcia (od 2)
                    for i, img in enumerate(images[1:], start=2):
                        img_url = img["url"]
                        img_path = variant_dir / f"{variant_slug}_{i}.jpg"
                        img_file_name = download_image(img_url, img_path)
                        image_urls.append(img_url)
                        image_file_names.append(img_file_name)
                else:
                    gray_file = ""

                # Producent
                manuf = variant.get("manufacturerAddress", {})
                manuf_address = ", ".join(filter(None, [
                    manuf.get("street", ""), manuf.get("postalCode", ""),
                    manuf.get("city", ""), manuf.get("country", "")
                ]))
                manufacturer_info = ", ".join(filter(None, [
                    manuf.get("company", ""), manuf_address, manuf.get("webContactInformation", "")
                ])) if manuf else ""

                simplified_data = {
                    "Brand": brand,
                    "Product Name": f"{brand_line} {base_name}".strip(),
                    "Product Family": product_data.get("productFamily", {}).get("name", ""),
                    "Variant Name": variant_name,
                    "Price": variant.get("priceData", {}).get("formattedValue", ""),
                    "Volume": f"{variant.get('numberContentUnits', '')} {variant.get('contentUnitOfBaseNumberContentUnits', '')}",
                    "Description": product_data.get("description", ""),
                    "Application": product_data.get("application", ""),
                    "Ingredients": product_data.get("ingredients", ""),
                    "Warnings": ", ".join(variant.get("safetyInformationCodes", [])),
                    "Bullet Points": " | ".join(product_data.get("bulletPoints", [])),
                    "Breadcrumbs": breadcrumb_str,
                    "Variant Image (Preview)": swatch_url,
                    "Main Image": image_urls[0] if image_urls else "",
                    "Main Image (Gray)": image_file_names[1] if len(image_file_names) > 1 else "",
                    "All Images": " | ".join(image_urls),
                    "Manufacturer Info": manufacturer_info
                }

                for idx, image_file_name in enumerate(image_file_names):
                    column = f"Image {idx + 1}"
                    simplified_data[column] = image_file_name
                    if column not in fieldnames:
                        fieldnames.append(column)
                        writer.fieldnames = fieldnames

                writer.writerow(simplified_data)

            print(f"✅ Dodano {len(variants)} wariantów z ID: {product_id}")
