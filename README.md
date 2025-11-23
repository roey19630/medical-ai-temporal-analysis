# 🏥 Clinical Temporal Data Management Tool

A Python-based command-line tool for managing **temporal clinical data**.  
Supports value lookup, history exploration, editing, and deletion while keeping full temporal consistency.

The system loads a clinical dataset (Excel) and a LOINC dictionary (CSV), and provides interactive operations using transaction-time and valid-time logic.

---

## ⚙️ Features

### 🔍 Value Search  
Query a patient’s lab result at a specific valid-time while respecting:
- Transaction-time constraints  
- Deletions and temporal updates  
- LOINC common name lookup

### 📚 History Search  
Display all versions of a patient’s measurement with timestamp filtering.

### ✏️ Edit Value  
Add updated lab values while automatically recording:
- New Value  
- Last Update timestamp

### 🗑 Delete Entry  
Soft-deletion using temporal flags:
- `Deleted = True`  
- `Delete_time = timestamp`

---

## 📁 Project Structure

```
main.py                     → Main application (menu & logic)
project_db.xlsx             → Clinical temporal dataset
Loinc.csv                   → LOINC code dictionary
```

---

## 🧰 Requirements

```
pip install pandas
```

---

## ▶️ Run the Application

```
python main.py
```

The interactive menu will appear:
```
1. Search Value
2. Search History
3. Edit Row
4. Delete Row
5. Exit
```

---

## 📌 Notes
- The dataset uses **valid-time** and **transaction-time** fields.  
- Bug fix applied to ensure correct retrieval of latest transaction record during same-time conflicts.  
  (See line 121 in `main.py`)  :contentReference[oaicite:1]{index=1}

---

## 📬 Contact
Feel free to reach out for questions or collaboration.
