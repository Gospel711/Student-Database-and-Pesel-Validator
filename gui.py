import tkinter as tk
from tkinter import messagebox, ttk

from database import StudentDatabase
from storage import load_from_file, save_to_file
from student import Student
from pesel_validator import validate_pesel


# -----------------------------
# DARK MODE COLOURS
# -----------------------------
BG = "#1e1e1e"
PANEL = "#2d2d2d"
TEXT = "#ffffff"
BTN = "#3a3a3a"
BTN_HOVER = "#505050"
ACCENT_BLUE = "#4aa3ff"
ACCENT_GREEN = "#4dff88"
ACCENT_RED = "#ff4d4d"
ACCENT_PURPLE = "#c77dff"


class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Database")
        self.root.geometry("800x600")
        self.root.configure(bg=BG)

        # Load database
        self.db = StudentDatabase()
        self.db.students = load_from_file()

        # Main frame
        self.main_frame = tk.Frame(self.root, bg=BG)
        self.main_frame.pack(fill="both", expand=True)

        self.show_main_menu()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # -------------------------------------------------
    # MAIN MENU
    # -------------------------------------------------
    def show_main_menu(self):
        self.clear_frame()

        tk.Label(
            self.main_frame,
            text="Student Database",
            font=("Arial", 28, "bold"),
            fg=ACCENT_BLUE,
            bg=BG
        ).pack(pady=20)

        buttons = [
            ("1. Add Student", self.show_add_student),
            ("2. Display All Students", self.show_student_list),
            ("3. Search by Last Name", self.show_search_lastname),
            ("4. Search by PESEL", self.show_search_pesel),
            ("5. Sort by Last Name", self.sort_by_lastname),
            ("6. Sort by PESEL", self.sort_by_pesel),
            ("7. Delete by Student ID", self.show_delete_student),
            ("8. Save and Exit", self.exit_program),
        ]

        for text, command in buttons:
            btn = tk.Button(
                self.main_frame,
                text=text,
                width=30,
                height=1,
                bg=BTN,
                fg=TEXT,
                activebackground=BTN_HOVER,
                activeforeground=TEXT,
                command=command
            )
            btn.pack(pady=6)

    # -------------------------------------------------
    # ADD STUDENT
    # -------------------------------------------------
    def show_add_student(self):
        self.clear_frame()

        tk.Label(
            self.main_frame,
            text="Add Student",
            font=("Arial", 24),
            fg=ACCENT_GREEN,
            bg=BG
        ).pack(pady=10)

        labels = ["First Name", "Last Name", "Address", "Student ID", "PESEL", "Gender"]
        self.entries = {}

        for label in labels:
            tk.Label(self.main_frame, text=label, fg=TEXT, bg=BG).pack()
            entry = tk.Entry(self.main_frame, bg=PANEL, fg=TEXT, insertbackground=TEXT)
            entry.pack()
            self.entries[label] = entry

        tk.Button(
            self.main_frame,
            text="Submit",
            bg=ACCENT_GREEN,
            fg="black",
            command=self.add_student
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Back",
            bg=ACCENT_RED,
            fg="black",
            command=self.show_main_menu
        ).pack()

    def add_student(self):
        first = self.entries["First Name"].get()
        last = self.entries["Last Name"].get()
        address = self.entries["Address"].get()
        sid = self.entries["Student ID"].get()
        pesel = self.entries["PESEL"].get()
        gender = self.entries["Gender"].get()

        if not validate_pesel(pesel):
            messagebox.showerror("Error", "Invalid PESEL")
            return

        student = Student(first, last, address, sid, pesel, gender)
        self.db.add_student(student)
        save_to_file(self.db.get_all_students())

        messagebox.showinfo("Success", "Student added successfully")

    # -------------------------------------------------
    # DISPLAY STUDENTS
    # -------------------------------------------------
    def show_student_list(self):
        self.clear_frame()

        tk.Label(
            self.main_frame,
            text="Student List",
            font=("Arial", 24),
            fg=ACCENT_PURPLE,
            bg=BG
        ).pack(pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=PANEL,
                        foreground=TEXT,
                        fieldbackground=PANEL,
                        rowheight=28)
        style.configure("Treeview.Heading",
                        background=BTN,
                        foreground=TEXT)

        self.tree = ttk.Treeview(
            self.main_frame,
            columns=("No", "First", "Last", "ID"),
            show="headings",
            height=15
        )

        self.tree.heading("No", text="#")
        self.tree.heading("First", text="First Name")
        self.tree.heading("Last", text="Last Name")
        self.tree.heading("ID", text="Student ID")

        self.tree.column("No", width=40, anchor="center")
        self.tree.column("First", width=200)
        self.tree.column("Last", width=200)
        self.tree.column("ID", width=150)

        self.tree.pack(fill="both", expand=True)

        students_sorted = sorted(
            self.db.get_all_students(),
            key=lambda s: (s.last_name.lower(), s.first_name.lower())
        )

        for index, s in enumerate(students_sorted, start=1):
            self.tree.insert("", "end", values=(index, s.first_name, s.last_name, s.student_id))

        tk.Button(
            self.main_frame,
            text="View Details",
            bg=ACCENT_GREEN,
            fg="black",
            command=self.show_student_details
        ).pack(pady=5)

        tk.Button(
            self.main_frame,
            text="Back",
            bg=ACCENT_RED,
            fg="black",
            command=self.show_main_menu
        ).pack(pady=5)

    # -------------------------------------------------
    # DETAILS POPUP + MODIFY STUDENT
    # -------------------------------------------------
    def show_student_details(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a student first.")
            return

        _, first, last, sid = self.tree.item(selected, "values")

        student = next(
            (s for s in self.db.get_all_students()
             if s.first_name == first and s.last_name == last and s.student_id == sid),
            None
        )

        if not student:
            messagebox.showerror("Error", "Student not found.")
            return

        win = tk.Toplevel(self.root)
        win.title("Student Details")
        win.geometry("500x450")
        win.configure(bg=BG)

        tk.Label(
            win,
            text="Student Details",
            font=("Arial", 20),
            fg=ACCENT_BLUE,
            bg=BG
        ).pack(pady=10)

        table = ttk.Treeview(win, columns=("Field", "Value"), show="headings", height=6)
        table.heading("Field", text="Field")
        table.heading("Value", text="Value")

        table.column("Field", width=150)
        table.column("Value", width=300)

        table.pack(pady=10)

        table.insert("", "end", values=("First Name", student.first_name))
        table.insert("", "end", values=("Last Name", student.last_name))
        table.insert("", "end", values=("Address", student.address))
        table.insert("", "end", values=("Student ID", student.student_id))
        table.insert("", "end", values=("PESEL", student.pesel))
        table.insert("", "end", values=("Gender", student.gender))

        tk.Button(
            win,
            text="Modify Student",
            bg=ACCENT_GREEN,
            fg="black",
            command=lambda: self.modify_student_popup(win, student)
        ).pack(pady=10)

    # -------------------------------------------------
    # MODIFY STUDENT INSIDE POPUP
    # -------------------------------------------------
    def modify_student_popup(self, parent, student):
        for widget in parent.winfo_children():
            widget.destroy()

        tk.Label(
            parent,
            text="Modify Student",
            font=("Arial", 20),
            fg=ACCENT_GREEN,
            bg=BG
        ).pack(pady=10)

        fields = ["First Name", "Last Name", "Address", "Student ID", "PESEL", "Gender"]
        values = [
            student.first_name,
            student.last_name,
            student.address,
            student.student_id,
            student.pesel,
            student.gender
        ]

        self.mod_entries = {}

        for label, value in zip(fields, values):
            tk.Label(parent, text=label, fg=TEXT, bg=BG).pack()
            entry = tk.Entry(parent, bg=PANEL, fg=TEXT, insertbackground=TEXT)
            entry.insert(0, value)
            entry.pack()
            self.mod_entries[label] = entry

        tk.Button(
            parent,
            text="Save Changes",
            bg=ACCENT_GREEN,
            fg="black",
            command=lambda: self.save_student_changes(parent, student)
        ).pack(pady=10)

        tk.Button(
            parent,
            text="Cancel",
            bg=ACCENT_RED,
            fg="black",
            command=parent.destroy
        ).pack()

    def save_student_changes(self, parent, student):
        student.first_name = self.mod_entries["First Name"].get()
        student.last_name = self.mod_entries["Last Name"].get()
        student.address = self.mod_entries["Address"].get()
        student.student_id = self.mod_entries["Student ID"].get()
        student.pesel = self.mod_entries["PESEL"].get()
        student.gender = self.mod_entries["Gender"].get()

        save_to_file(self.db.get_all_students())
        messagebox.showinfo("Success", "Student updated successfully")
        parent.destroy()

    # -------------------------------------------------
    # SEARCH BY LAST NAME
    # -------------------------------------------------
    def show_search_lastname(self):
        self.clear_frame()

        tk.Label(
            self.main_frame,
            text="Search by Last Name",
            font=("Arial", 22),
            fg=ACCENT_BLUE,
            bg=BG
        ).pack(pady=10)

        entry = tk.Entry(self.main_frame, bg=PANEL, fg=TEXT, insertbackground=TEXT)
        entry.pack(pady=5)

        def search():
            last = entry.get()
            results = self.db.find_by_last_name(last)

            if not results:
                messagebox.showinfo("Result", "No students found.")
                return

            names = "\n".join([f"{s.first_name} {s.last_name}" for s in results])
            messagebox.showinfo("Results", names)

        tk.Button(self.main_frame, text="Search", bg=ACCENT_GREEN, fg="black", command=search).pack(pady=10)
        tk.Button(self.main_frame, text="Back", bg=ACCENT_RED, fg="black", command=self.show_main_menu).pack()

    # -------------------------------------------------
    # SEARCH BY PESEL
    # -------------------------------------------------
    def show_search_pesel(self):
        self.clear_frame()

        tk.Label(
            self.main_frame,
            text="Search by PESEL",
            font=("Arial", 22),
            fg=ACCENT_BLUE,
            bg=BG
        ).pack(pady=10)

        entry = tk.Entry(self.main_frame, bg=PANEL, fg=TEXT, insertbackground=TEXT)
        entry.pack(pady=5)

        def search():
            pesel = entry.get()
            results = self.db.find_by_pesel(pesel)

            if not results:
                messagebox.showinfo("Result", "No students found.")
                return

            names = "\n".join([f"{s.first_name} {s.last_name}" for s in results])
            messagebox.showinfo("Results", names)

        tk.Button(self.main_frame, text="Search", bg=ACCENT_GREEN, fg="black", command=search).pack(pady=10)
        tk.Button(self.main_frame, text="Back", bg=ACCENT_RED, fg="black", command=self.show_main_menu).pack()

    # -------------------------------------------------
    # SORTING
    # -------------------------------------------------
    def sort_by_lastname(self):
        self.db.sort_by_last_name()
        save_to_file(self.db.get_all_students())
        messagebox.showinfo("Success", "Students sorted by last name.")
        self.show_main_menu()

    def sort_by_pesel(self):
        self.db.sort_by_pesel()
        save_to_file(self.db.get_all_students())
        messagebox.showinfo("Success", "Students sorted by PESEL.")
        self.show_main_menu()

    # -------------------------------------------------
    # DELETE BY STUDENT ID
    # -------------------------------------------------
    def show_delete_student(self):
        self.clear_frame()

        tk.Label(
            self.main_frame,
            text="Delete by Student ID",
            font=("Arial", 22),
            fg=ACCENT_RED,
            bg=BG
        ).pack(pady=10)

        entry = tk.Entry(self.main_frame, bg=PANEL, fg=TEXT, insertbackground=TEXT)
        entry.pack(pady=5)

        def delete():
            sid = entry.get()
            self.db.delete_by_id(sid)
            save_to_file(self.db.get_all_students())
            messagebox.showinfo("Success", "Deleted if existed.")

        tk.Button(self.main_frame, text="Delete", bg=ACCENT_RED, fg="black", command=delete).pack(pady=10)
        tk.Button(self.main_frame, text="Back", bg=BTN, fg=TEXT, command=self.show_main_menu).pack()

    # -------------------------------------------------
    # SAVE & EXIT
    # -------------------------------------------------
    def exit_program(self):
        save_to_file(self.db.get_all_students())
        self.root.quit()


def run_gui():
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
