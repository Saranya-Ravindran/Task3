# Task 3: Extracting and Organizing Sports Results:

# Project Overview :
This project focuses on automating the extraction of tabular data from PDFs available on official sports websites, specifically for athletics and swimming events. 
The primary goals are:
Automated Extraction: Programmatically download and extract tables from multi-page PDFs.
Data Organization: Compile the extracted data into structured Excel files.
Manual Refinement: Further organize and clean the data manually to produce final, polished Excel sheets.

# Source Websites
Athletics Results: https://indianathletics.in/results/
Swimming Results: https://www.swimming.org.in/38th-national-games-2025/#results

# Tools & Libraries Used
Python 3.11

# Libraries:
requests: For handling HTTP requests.
BeautifulSoup: For parsing HTML content.
pdfplumber: For extracting tables from PDF files.
pandas: For data manipulation and Excel file creation.
openpyxl: For Excel file operations.

# Repository Structure
Task3/
├── afi_results_pdfs/          # Downloaded athletics PDFs
├── sfi_results_pdfs/          # Downloaded swimming PDFs
├── AFI_All_Results.xlsx       # Combined athletics results (auto-extracted)
├── SFI_All_Results.xlsx       # Combined swimming results (auto-extracted)
├── Final_AFI_results.xlsx     # Final organized athletics results (manually refined)
├── Final_SFI_results.xlsx     # Final organized swimming results (manually refined)
├── athletics.py               # Script for athletics data extraction
├── swimming.py                # Script for swimming data extraction
└── README.md                  # Project documentation

# How to Run the Scripts
 
Clone the Repository:
git clone https://github.com/Saranya-Ravindran/Task3.git
cd Task3

Install Required Libraries:
Ensure you have Python 3.11 installed. Then, install the necessary libraries:

pip install requests beautifulsoup4 pdfplumber pandas openpyxl

Run the Scripts:

For athletics data:
python athletics.py

For swimming data:
python swimming.py

These scripts will:
Scrape PDF links from the respective websites.
Download the PDFs into their designated folders.
Extract tables from each PDF.
Combine all extracted tables into a single Excel file (AFI_All_Results.xlsx or SFI_All_Results.xlsx).

Manual Refinement:
After automatic extraction, the combined Excel files may require manual cleaning and organization. The refined versions are saved as Final_AFI_results.xlsx and Final_SFI_results.xlsx.

# Notes
Handling Missing CropBox:
Some PDFs might lack a CropBox attribute, leading to warnings. To suppress these warnings:

import warnings
warnings.filterwarnings("ignore", message=".*CropBox missing.*")

Error Handling:
The scripts include basic error handling to manage issues like network timeouts or PDF parsing errors. Ensure a stable internet connection when running the scripts.
