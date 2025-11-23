# 🧬 Medical AI Temporal Analysis

A Python-based temporal database management tool for medical records.
Supports: temporal queries (transaction vs valid time), history search, logical deletion with timestamps, editing medical records, and LOINC metadata enrichment.

---

## 📁 Project Structure

* **project_ai_medicine.py** – Main program
* **project_db_test_DEFENSE_25_final.xlsx** – Medical temporal dataset
* **project_db_2024.xlsx** – Additional dataset
* **Loinc.zip** – Compressed LOINC dictionary (because GitHub cannot accept the CSV size)

---

## 🛠 Installation

Install dependencies:
pip install pandas openpyxl

---

## ▶️ Running the Program

Run the main script:
python project_ai_medicine.py

The program will open an interactive command-line menu supporting:
• Value search
• History search
• Row editing
• Row deletion

---

## ⚠️ Important: LOINC File Extraction

The repository includes the LOINC dictionary **as Loinc.zip** due to GitHub’s file-size limits.

Before running the program:

1. Extract **Loinc.zip**
2. Ensure **Loinc.csv** is placed in the **project root directory**
3. The script will automatically load it when needed

---

## 📝 Notes

* The LOINC dataset is very large, so it is zipped for storage
* The program expects all files to be located in the **root directory** (same folder as the .py script)

---

## 📞 Contact

Feel free to reach out for questions or collaboration.

---
