# 🏥 AI Medical Temporal Database System  
An interactive Python-based system for managing **temporal medical data**, including searching historical medical values, editing records, handling deletions, and retrieving LOINC metadata.

The project implements a miniature **temporal database**, enabling querying of past states based on transaction time and valid time.

---

## ✨ Features

### • Temporal Value Search  
Search patient data using:
- First name / last name  
- LOINC code  
- Valid start date & time  
- Transaction-time filtering  
Includes automatic retrieval of **LOINC common names**.

### • Temporal History Tracking  
Query full history of a medical measurement over:
- Custom time intervals  
- Specific dates or timestamps

### • Edit & Update Records  
Modify values with proper:
- `Last Update` timestamp  
- `New Value` tracking

### • Logical Deletion  
Mark rows as deleted while keeping them queryable according to temporal rules.

---

## 📁 Files Included
```
ai-medical-temporal-db/
│── project.py
│── project_db_test_DEFENSE_25_final.xlsx
│── Loinc.csv
│── README.md
```

---

## 🛠️ How to Run

Install dependencies (only pandas required):

```bash
pip install pandas
```

Run the program:

```bash
python project.py
```

The menu will appear in the console automatically.

---

## 📊 Dataset Notes
- `project_db_test_DEFENSE_25_final.xlsx` contains the temporal medical records.
- `Loinc.csv` provides mapping from LOINC codes to their common names.

---

## 📬 Contact
Feel free to reach out for questions or collaboration.
