from student import Student
from pesel_validator import validate_pesel

class StudentDatabase:
    """
    Stores all students in memory and provides
    operations for adding, searching, sorting, and deleting.
    """

    def __init__(self):
        self.students = []

    def add_student(self, student: Student):
        """
        Add a student after validating PESEL.
        """
        if not validate_pesel(student.pesel):
            raise ValueError("Invalid PESEL number.")
        self.students.append(student)

    def get_all_students(self):
        return self.students

    def find_by_last_name(self, last_name):
        """
        Case-insensitive search by last name.
        """
        return [s for s in self.students if s.last_name.lower() == last_name.lower()]

    def find_by_pesel(self, pesel):
        """
        Search by PESEL (exact match).
        """
        return [s for s in self.students if s.pesel == pesel]

    def delete_by_id(self, student_id):
        """
        Delete student with matching ID.
        """
        self.students = [s for s in self.students if s.student_id != student_id]

    def sort_by_last_name(self):
        """
        Sort students alphabetically by last name.
        """
        self.students.sort(key=lambda s: s.last_name.lower())

    def sort_by_pesel(self):
        """
        Sort students numerically by PESEL.
        """
        self.students.sort(key=lambda s: s.pesel)