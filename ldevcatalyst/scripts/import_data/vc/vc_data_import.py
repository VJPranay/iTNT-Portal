import csv
from django.db import transaction
from datarepo.models import District, State, AreaOfInterest, PreferredInvestmentStage
from registrations.models import VCRegistrations  # Assuming VCRegistrations is in a 'vc' app
import uuid


@transaction.atomic
def import_vc_data(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            # Create or get District and State objects
            district, _ = District.objects.get_or_create(name=row[7])
            state, _ = State.objects.get_or_create(name=row[8], defaults={'district': district})

            # Create or get Area of Interest objects
            areas_of_interest_names = row[9].split(',')
            areas_of_interest = []
            for area_name in areas_of_interest_names:
                area_obj, _ = AreaOfInterest.objects.get_or_create(name=area_name.strip())
                areas_of_interest.append(area_obj)

            # Create or get Preferred Investment Stage objects
            funding_stages_names = row[10].split(',')
            funding_stages = []
            for stage_name in funding_stages_names:
                stage_obj, _ = PreferredInvestmentStage.objects.get_or_create(name=stage_name.strip())
                funding_stages.append(stage_obj)

            # Generate a unique registration ID
            reg_id = 'VCRG-' + str(uuid.uuid4())[:4].upper()

            # Create VCRegistrations object
            vc_registration = VCRegistrations.objects.create(
                partner_name=row[0],
                firm_name=row[1],
                email=row[2],
                mobile=row[3],
                district=district,
                state=state,
                company_website=row[11],
                linkedin_profile=row[12],
                registration_id=reg_id,
                data_source='csv'
            )

            # Add Area of Interest and Preferred Investment Stage
            vc_registration.area_of_interest.add(*areas_of_interest)
            vc_registration.funding_stage.add(*funding_stages)

            vc_registration.save()

    return 'Data imported successfully'

# Usage example
csv_file_path = '/opt/portal/iTNT-Portal/ldevcatalyst/scripts/import_data/vc/latest_vc.csv'  # Update with your actual CSV file path
result_message = import_vc_data(csv_file_path)
print(result_message)
