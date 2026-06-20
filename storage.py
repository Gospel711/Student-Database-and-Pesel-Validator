import json
from student import Student

def save_to_file(students, filename="students.json"):
    """
    Save list of Student objects to a JSON file.
    """
    data = [s.to_dict() for s in students]
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_from_file(filename="students.json"):
    """
    Load students from JSON file.
    Returns a list of Student objects.
    """
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return [Student.from_dict(item) for item in data]
    except FileNotFoundError:
        return []