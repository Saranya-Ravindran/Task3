import warnings
warnings.filterwarnings("ignore", message=".*CropBox missing.*")
import requests
from bs4 import BeautifulSoup
import os
import pdfplumber
import pandas as pd
BASE_URL = "https://indianathletics.in/results/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
PDF_DIR = "afi_results_pdfs"
EXCEL_OUTPUT = "AFI_All_Results.xlsx"

os.makedirs(PDF_DIR, exist_ok=True)
print("Fetching PDF links...")
response = requests.get(BASE_URL, headers=HEADERS)
soup = BeautifulSoup(response.content, "html.parser")
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
        pdf_resp = requests.get(pdf_url, headers=HEADERS)
        with open(pdf_path, 'wb') as f:
            f.write(pdf_resp.content)
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
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    combined_df.to_excel(EXCEL_OUTPUT, index=False)
    print(f"\nAll results saved to: {EXCEL_OUTPUT}")
else:
    print("No tables were extracted.")
