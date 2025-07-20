class Student:
    """Represents a student."""
    def __init__(self, student_id, username, password, email, first_name, last_name, age, sex, department, year, semester):
        self.student_id = student_id
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.department = department
        self.year = year
        self.semester = semester

class Admin:
    """Represents an administrator."""
    def __init__(self, admin_id, username, password, email, first_name, last_name, sex, age, position):
        self.admin_id = admin_id
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.age = age
        self.position = position

class Complaint:
    """Class representing a complaint."""
    def __init__(self, complaint_id, admin_id, student_id, description, category, status, submission_date, 
                 assigned_to, resolution_details, resolution_date):
        self.complaint_id = complaint_id
        self.admin_id = admin_id
        self.student_id = student_id
        self.description = description
        self.category = category
        self.status = status
        self.submission_date = submission_date
        self.assigned_to = assigned_to
        self.resolution_details = resolution_details
        self.resolution_date = resolution_date