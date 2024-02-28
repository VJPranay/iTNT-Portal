import csv
import os
from ldevcatalyst.settings import BASE_DIR
from datarepo.models import Institution,District
from django.db import IntegrityError

def add_institution_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file,delimiter='\t')
        for row in reader:
            district_name = row[0]
            college_name = row[2]
            try:
                district_info = District.objects.get(name=district_name)
                try:
                    new_institution = Institution.objects.create(district_id = district_info.id,name=college_name)
                    new_institution.save()
                except IntegrityError as e:
                    print(e)
            except District.DoesNotExist:
                print(f"{district_name} doesnt exist in DB")
csv_file_path = os.path.join(BASE_DIR, "scripts/colleges/colleges.tsv")
add_institution_from_csv(csv_file_path)