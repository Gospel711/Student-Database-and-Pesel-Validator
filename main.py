from database import StudentDatabase
from storage import save_to_file, load_from_file
from cli import get_student_input
from student import Student

# Colours
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

def pause_menu():
    print(f"\n{YELLOW}1. Return to menu{RESET}")
    print(f"2. Exit program")
    choice = input("Choose: ")
    if choice == "2":
        print("Goodbye.")
        exit()

def show_main_menu():
    print(f"\n{CYAN}--- Student Database Menu ---{RESET}")
    print("1. Add student")
    print("2. Display all students")
    print("3. Search by last name")
    print("4. Search by PESEL")
    print("5. Sort by last name")
    print("6. Sort by PESEL")
    print("7. Delete by student ID")
    print("8. Save and Exit")

def show_student_table(student: Student):
    print(f"\n{MAGENTA}-----------------------------------------")
    print("| FIELD        | VALUE                  |")
    print("-----------------------------------------")
    print(f"| First Name   | {student.first_name:<22} |")
    print(f"| Last Name    | {student.last_name:<22} |")
    print(f"| Address      | {student.address:<22} |")
    print(f"| Student ID   | {student.student_id:<22} |")
    print(f"| PESEL        | {student.pesel:<22} |")
    print(f"| Gender       | {student.gender:<22} |")
    print("-----------------------------------------{RESET}")

def modify_student(student: Student):
    print(f"\n{CYAN}--- Modify Student ---{RESET}")
    print("1. First name")
    print("2. Last name")
    print("3. Address")
    print("4. Student ID")
    print("5. PESEL")
    print("6. Gender")
    print("7. Cancel")

    choice = input("Choose field: ")

    if choice == "1":
        student.first_name = input("New first name: ")
    elif choice == "2":
        student.last_name = input("New last name: ")
    elif choice == "3":
        student.address = input("New address: ")
    elif choice == "4":
        student.student_id = input("New student ID: ")
    elif choice == "5":
        student.pesel = input("New PESEL: ")
    elif choice == "6":
        student.gender = input("New gender: ")
    elif choice == "7":
        return
    else:
        print(f"{RED}Invalid choice.{RESET}")

    print(f"{GREEN}Student updated successfully!{RESET}")

def main():
    db = StudentDatabase()
    db.students = load_from_file()

    while True:
        show_main_menu()
        choice = input("Choose an option: ")

        # ADD STUDENT
        if choice == "1":
            student = get_student_input()
            if student is None:
                print("Returning to menu.")
                continue
            try:
                db.add_student(student)
                print(f"{GREEN}Student added.{RESET}")
            except ValueError as e:
                print(f"{RED}{e}{RESET}")
            pause_menu()

        # DISPLAY ALL STUDENTS
        elif choice == "2":
            students = db.get_all_students()
            if not students:
                print(f"{RED}No students in the database.{RESET}")
                pause_menu()
                continue

            students_sorted = sorted(
                students,
                key=lambda s: (s.last_name.lower(), s.first_name.lower())
            )

            print(f"\n{MAGENTA}--- Student List ---{RESET}")
            for index, s in enumerate(students_sorted, start=1):
                print(f"{index}. {s.first_name} {s.last_name}")

            print("\nSelect a student number to view details, or 0 to return.")
            sel = input("Choose: ")

            if sel == "0":
                continue

            if not sel.isdigit() or int(sel) < 1 or int(sel) > len(students_sorted):
                print(f"{RED}Invalid selection.{RESET}")
                pause_menu()
                continue

            selected_student = students_sorted[int(sel) - 1]
            show_student_table(selected_student)

            print("\n1. Modify student")
            print("2. Delete student")
            print("3. Return to list")

            action = input("Choose: ")

            if action == "1":
                modify_student(selected_student)
            elif action == "2":
                db.delete_by_id(selected_student.student_id)
                print(f"{GREEN}Student deleted.{RESET}")

            pause_menu()

        # SEARCH BY LAST NAME
        elif choice == "3":
            last = input("Enter last name: ")
            results = db.find_by_last_name(last)
            if not results:
                print(f"{RED}No students found.{RESET}")
            else:
                for s in results:
                    print(f"{s.first_name} {s.last_name}")
            pause_menu()

        # SEARCH BY PESEL
        elif choice == "4":
            pesel = input("Enter PESEL: ")
            results = db.find_by_pesel(pesel)
            if not results:
                print(f"{RED}No students found.{RESET}")
            else:
                for s in results:
                    print(f"{s.first_name} {s.last_name}")
            pause_menu()

        # SORTING
        elif choice == "5":
            db.sort_by_last_name()
            print(f"{GREEN}Sorted by last name.{RESET}")
            pause_menu()

        elif choice == "6":
            db.sort_by_pesel()
            print(f"{GREEN}Sorted by PESEL.{RESET}")
            pause_menu()

        # DELETE BY ID
        elif choice == "7":
            sid = input("Enter student ID to delete: ")
            db.delete_by_id(sid)
            print(f"{GREEN}Deleted if existed.{RESET}")
            pause_menu()

        # SAVE AND EXIT
        elif choice == "8":
            save_to_file(db.get_all_students())
            print(f"{GREEN}Saved. Exiting.{RESET}")
            break

        else:
            print(f"{RED}Invalid option.{RESET}")
            pause_menu()

if __name__ == "__main__":
    main()