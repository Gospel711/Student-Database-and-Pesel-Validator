from student import Student
from pesel_validator import validate_pesel

def show_menu():
    print("\n--- Student Database Menu ---")
    print("1. Add student")
    print("2. Display all students")
    print("3. Search by last name")
    print("4. Search by PESEL")
    print("5. Sort by last name")
    print("6. Sort by PESEL")
    print("7. Delete by student ID")
    print("8. Save and Exit")

def get_student_input():
    """
    Collect user input for creating a new student.
    First PESEL attempt is normal.
    If invalid, THEN show retry/return options.
    """

    first_name = input("First name: ")
    last_name = input("Last name: ")
    address = input("Address: ")
    student_id = input("Student ID: ")

    # First attempt (normal)
    pesel = input("PESEL: ")

    # If first attempt invalid → show menu
    while not validate_pesel(pesel):
        print("\nInvalid PESEL.")
        print("1. Retry")
        print("2. Return to main menu")

        choice = input("Choose: ")

        if choice == "2":
            return None  # return to menu

        if choice == "1":
            pesel = input("PESEL: ")
        else:
            print("Invalid choice.")

    gender = input("Gender: ")

    return Student(first_name, last_name, address, student_id, pesel, gender)