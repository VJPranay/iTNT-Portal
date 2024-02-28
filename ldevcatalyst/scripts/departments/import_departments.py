import csv
import os
from ldevcatalyst.settings import BASE_DIR
from datarepo.models import Department
def add_departments_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            department_name = row[0]
            # Assuming Department model has a field named 'name'
            department = Department.objects.create(name=department_name)
            department.save()
            print(row[0])
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_file_path = os.path.join(BASE_DIR, "scripts/departments/departments.csv")
add_departments_from_csv(csv_file_path)