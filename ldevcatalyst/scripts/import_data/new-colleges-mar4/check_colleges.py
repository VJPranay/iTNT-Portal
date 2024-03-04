import csv
import os
from ldevcatalyst.settings import BASE_DIR
from datarepo.models import Institution,District
from django.db import IntegrityError

def add_institution_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file,delimiter=',')
        for row in reader:
            district_name = row[0]
            try:
                district_info = District.objects.get(name=district_name)
                new_college = Institution.objects.create(
                name = row[1],
                district_id = district_info.id
                )
                new_college.save()
                print(new_college.id)
            except District.DoesNotExist:
                print(district_name," is not present in db")
            


file_path = '/opt/portal/iTNT-Portal/ldevcatalyst/scripts/import_data/new-colleges-mar4/Eng_College_Name_Updated.csv'
add_institution_from_csv(file_path)