import csv
from datetime import datetime
from django.db import transaction
from django.db.utils import IntegrityError
from registrations.models import ResearcherRegistrations, PatentInfo, PublicationInfo
from datarepo.models import Department, Institution, District, State, AreaOfInterest
import uuid
from django.db.utils import DataError
@transaction.atomic
def import_researcher_data(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            try:
                try:
                    department_info = Department.objects.get(name=row[2])
                except Department.DoesNotExist:
                    department_info = Department.objects.create(name=row[2])
                    department_info.save()
                try:
                    state_info = State.objects.get(name=row[5])
                except State.DoesNotExist:
                    state_info = State.objects.create(name=row[5])
                    state_info.save()
                try:
                    district_info = District.objects.get(name=row[4])
                except District.DoesNotExist:
                    district_info = District.objects.create(name=row[4], state_id=state_info.id)
                    district_info.save()
                try:
                    institution_info = Institution.objects.get(name=row[3])
                except Institution.DoesNotExist:
                    institution_info = Institution.objects.create(
                        name=row[3],
                        district_id=district_info.id
                    )
                    institution_info.save()
                
                # Generate a unique registration ID
                reg_id = 'RCRG-' + str(uuid.uuid4())[:4].upper()
                
                try:
                    with transaction.atomic():
                        researcher = ResearcherRegistrations.objects.create(
                            name=row[0],
                            gender=1 if row[1] == 'Male' else 2 if row[1] == 'Female' else None,
                            department=department_info,
                            institution=institution_info,
                            district=district_info,
                            state=state_info,
                            email=row[6],
                            mobile=row[7],
                            highest_qualification=row[10],
                            data_source='csv',
                            registration_id=reg_id
                        )
                        researcher.save()
                        
                        # Add area of interest
                        
                        areas_of_interest = row[9].split(',')
                        for area_name in areas_of_interest:
                            print(area_name)
                            area_obj, created = AreaOfInterest.objects.get_or_create(name=area_name.strip())
                            researcher.area_of_interest.add(area_obj)

                        # Add patents
                        patents_data = zip(
                            row[15::4],
                            row[16::4],
                            row[17::4],
                            row[18::4]
                        )
                        for title, inventors, filing_date, status in patents_data:
                            patent = PatentInfo.objects.create(
                                title=title.strip(),
                                inventors=inventors.strip(),
                                status=status.strip(),
                            )
                            researcher.patents.add(patent)
                            researcher.save()

                        # Add publication
                        publication = PublicationInfo.objects.create(
                            title=row[11],
                            paper_link=row[12],
                            journal=row[13],
                        )
                        researcher.publications = publication

                        researcher.save()
                except IntegrityError:
                    # If a UNIQUE constraint fails, generate a new registration ID and retry
                    reg_id = 'RCRG-' + str(uuid.uuid4())[:4].upper()
                    continue
            except DataError:
                continue

    return 'Data imported successfully'

# Usage example
#csv_file_path = '/opt/portal/iTNT-Portal/ldevcatalyst/scripts/import_data/sme/3000sme.csv'
csv_file_path = '/Users/vj/itnt/iTNT-Portal/ldevcatalyst/scripts/import_data/sme/3000sme.csv'
result_message = import_researcher_data(csv_file_path)
print(result_message)
