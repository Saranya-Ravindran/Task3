import warnings
warnings.filterwarnings("ignore", message=".*CropBox missing.*")
import requests
from bs4 import BeautifulSoup
import os
import pdfplumber
import pandas as pd
BASE_URL = "https://www.swimming.org.in/38th-national-games-2025/#results"
HEADERS = {"User-Agent": "Mozilla/5.0"}
PDF_DIR = "sfi_results_pdfs"
EXCEL_OUTPUT = "SFI_All_Results.xlsx"

os.makedirs(PDF_DIR, exist_ok=True)
print("Fetching PDF links...")
try:
    response = requests.get(BASE_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
except requests.exceptions.RequestException as e:
    print(f"Error fetching base URL: {e}")
    raise SystemExit
pdf_links = []
for link in soup.find_all("a", href=True):
    href = link['href']
    if href.lower().endswith(".pdf"):
        full_url = requests.compat.urljoin(BASE_URL, href)
        pdf_links.append(full_url)

print(f"Found {len(pdf_links)} PDF files.")
for pdf_url in pdf_links:
    pdf_name = os.path.basename(pdf_url.split("?")[0])
    pdf_path = os.path.join(PDF_DIR, pdf_name)
    if not os.path.exists(pdf_path):
        print(f"Downloading: {pdf_name}")
        try:
            pdf_resp = requests.get(pdf_url, headers=HEADERS, timeout=20)
            pdf_resp.raise_for_status()
            with open(pdf_path, 'wb') as f:
                f.write(pdf_resp.content)
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {pdf_url}: {e}")
    else:
        print(f"Already downloaded: {pdf_name}")
all_dataframes = []

for pdf_file in os.listdir(PDF_DIR):
    if not pdf_file.endswith(".pdf"):
        continue
    pdf_path = os.path.join(PDF_DIR, pdf_file)
    print(f"Extracting tables from: {pdf_file}")

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                for table in tables:
                    if table and len(table) > 1:
                        raw_header = table[0]
                        header = []
                        used_names = set()
                        for i, col in enumerate(raw_header):
                            col = col.strip() if col else f"Column_{i}"
                            col = col.encode('ascii', 'ignore').decode('ascii')  # Remove emojis
                            if col == "" or col is None:
                                col = f"Column_{i}"
                            if col in used_names:
                                col = f"{col}_{i}"
                            used_names.add(col)
                            header.append(col)
                        df = pd.DataFrame(table[1:], columns=header)
                        df.insert(0, "Source File", pdf_file)
                        df.insert(1, "Page", page_number)

                        all_dataframes.append(df)
    except Exception as e:
        print(f"Error processing {pdf_file}: {e}")
if all_dataframes:
    try:
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        combined_df.to_excel(EXCEL_OUTPUT, index=False)
        print(f"\n All results saved to: {EXCEL_OUTPUT}")
    except Exception as e:
        print(f"Error saving Excel file: {e}")
else:
    print(" No tables were extracted.")
