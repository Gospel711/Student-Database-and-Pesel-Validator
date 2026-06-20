# 📘 Student Database Application

## 🎯 Overview

The **Student Database Application** is a Python‑based project that manages student records using both a **command‑line interface (CLI)** and a **Tkinter graphical user interface (GUI)**.  
It supports adding, viewing, searching, sorting, modifying, and deleting student data, with persistent storage handled through JSON files.

The GUI version features:

- 🌙 **Pure Tkinter Dark Mode**
- 🧾 **Full student table view**
- 🔍 **Search by last name or PESEL**
- ✏️ **Modify student inside a popup window**
- 🗂️ **Alphabetical + numerical ordering**
- 🧹 **Clean, modern styling**
- 💾 **Persistent storage**

This project is ideal for learning:

- GUI development with Tkinter
- Data validation (PESEL)
- Modular Python architecture
- File‑based persistence
- UX design for desktop apps

---

## 🏗️ Project Structure

```
Student-Database-and-Pesel-Validator/
│
├── gui.py                 # Tkinter GUI (dark mode + modify student)
├── main.py                # CLI version (optional)
├── student.py             # Student class
├── database.py            # StudentDatabase class
├── storage.py             # Save/load JSON functions
├── pesel_validator.py     # PESEL validation logic
├── cli.py                 # CLI input handling
├── students.json          # Persistent storage file
└── README.md              # Documentation
```

---

## 🚀 Features

### ✔ Add Student

Enter first name, last name, address, student ID, PESEL, and gender.

### ✔ Display All Students

Shows a sortable table with:

- Numerical index
- First name
- Last name
- Student ID

### ✔ View Full Details

Opens a popup window with a table of all fields.

### ✔ Modify Student

Inside the popup:

- Edit any field
- Save changes
- Automatically updates the database

### ✔ Search

- By last name
- By PESEL

### ✔ Sorting

- Alphabetically by last name
- Numerically by PESEL

### ✔ Delete Student

Remove a student by student ID.

### ✔ Dark Mode

A clean, modern dark theme using pure Tkinter:

- Dark backgrounds
- Light text
- Styled Treeview
- Accent colours

---

## 🖥️ Running the GUI

Make sure you have Python 3 installed.

Run:

```
python3 gui.py
```

The GUI will launch immediately.

---

## 🧪 Running the CLI (optional)

If you want to use the original CLI version:

```
python3 main.py
```

---

## 🧩 PESEL Validation

The project includes a custom PESEL validator that checks:

- Length (11 digits)
- Date encoding
- Checksum correctness

Invalid PESELs are rejected in both CLI and GUI.

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** (GUI)
- **JSON** (data storage)
- **OOP architecture**
- **Custom validation logic**

---

## 📌 Future Improvements (Optional)

These features can be added later:

- Icons for buttons
- Dark/light mode toggle
- SQLite database backend
- CSV export
- Dashboard with statistics
- Sidebar navigation
- Search suggestions

---

## 👤 Author

Developed by **Gospel**, a software engineering student focused on:

- System administration
- GUI development
- Clean UX
- Portfolio‑ready Python projects
