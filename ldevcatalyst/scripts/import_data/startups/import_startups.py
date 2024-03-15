import csv
import os
from ldevcatalyst.settings import BASE_DIR
from django.db import IntegrityError
from registrations.models import StartUpRegistrations
from datarepo.models import State,District,AreaOfInterest,PreferredInvestmentStage

def add_institution_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file,delimiter=',')
        for row in reader:
            startup_name = row[0]
            co_founder_count = row[1]
            state_name = row[2]
            district_name = row[3]
            team_size = row[4]
            email = row[5]
            mobile = row[6]
            website = row[7]
            dpiit_number = row[8]
            area_of_interest = row[9]
            required_amount = row[10]
            funding_stage = row[11]
            description = row[12]
            state_info = None
            try:
                state_info = State.objects.get(name=state_name)
            except State.DoesNotExist:
                # state_info = State.objects.create(name=state_name)
                # state_info.save()
                print(state_info)
                continue
            district_info = None
            try:
                district_info = District.objects.get(name=district_name)
            except District.DoesNotExist:
                print(district_name)
                continue
                # district_info = District.objects.create(name=district_name)
                # district_info.save()  
            area_of_interest_info = None
            try:
                area_of_interest_info = AreaOfInterest.objects.get(name=area_of_interest)
            except AreaOfInterest.DoesNotExist:
                area_of_interest_info = AreaOfInterest.objects.create(name=area_of_interest)
                area_of_interest_info.save()
            funding_stage_info = None
            try:
                funding_stage_info = PreferredInvestmentStage.objects.get(name=funding_stage)
            except PreferredInvestmentStage.DoesNotExist:
                # funding_stage_info = PreferredInvestmentStage.objects.create(name=funding_stage)
                # funding_stage_info.save()
                print(funding_stage)
                continue
                
            startup_registration = StartUpRegistrations.objects.create(
                name = startup_name,
                co_founder_count = co_founder_count,
                state_id = state_info.id,
                district_id = district_info.id,
                email = email,
                mobile = mobile,
                website = website,
                dpiit_number = dpiit_number,
                area_of_interest_id = area_of_interest_info.id,
                description = description,
                required_amount = required_amount,
                funding_stage_id=funding_stage_info.id
            )
            startup_registration.save()

file_path = '/opt/portal/iTNT-Portal/ldevcatalyst/scripts/import_data/startups/startup_data.csv'
#file_path = '/Users/vj/itnt/iTNT-Portal/ldevcatalyst/scripts/import_data/startups/startup_data.csv'
add_institution_from_csv(file_path)