class Student:
    """
    Represents a single student record.
    Stores all required fields and provides
    conversion to/from dictionary for JSON storage.
    """

    def __init__(self, first_name, last_name, address, student_id, pesel, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.student_id = student_id
        self.pesel = pesel
        self.gender = gender

    def to_dict(self):
        """
        Convert the Student object into a dictionary.
        Used when saving to JSON.
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "student_id": self.student_id,
            "pesel": self.pesel,
            "gender": self.gender
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Student object from a dictionary.
        Used when loading from JSON.
        """
        return Student(
            data["first_name"],
            data["last_name"],
            data["address"],
            data["student_id"],
            data["pesel"],
            data["gender"]
        )