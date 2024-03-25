import csv
from django.utils import timezone
from registrations.models import VCRegistrations, StartUpRegistrations
from meetings.models import MeetingRequests
import uuid

def create_meeting_requests_from_tsv(file_path):
    with open(file_path, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')  # Assuming TSV file format
        next(reader)  # Skip the header row if it exists
        for row in reader:
            firm_name = row[0].strip()  # Trim and get firm name from TSV
            partner_name = row[1].strip()  # Trim and get partner name from TSV
            partner_email = row[2].strip()  # Trim and get partner email from TSV
            partner_mobile = row[3].strip()  # Trim and get partner mobile from TSV
            startup_name = row[4].strip()  # Trim and get startup name from TSV
            startup_email = row[5].strip()  # Trim and get startup email from TSV
            startup_mobile = row[6].strip()  # Trim and get startup mobile from TSV
            location = row[7].split(' - ')[0].strip()  # Extract location from 'Suit 1 (12.00pm-12.15pm)' format
            meeting_time_str = row[7].split('(')[1].split(')')[0].strip()  # Extract meeting time from '12.00pm-12.15pm' format
            next_level = True if row[8].strip().lower() == 'yes' else False  # Convert 'Yes' to True, else False

            # Parse meeting time from string
            meeting_time = timezone.datetime.strptime(meeting_time_str, '%I.%M%p').time()  # Example format: '12.00pm'

            # Check if VC exists based on email (case insensitive)
            vc = VCRegistrations.objects.filter(email__iexact=partner_email).first()

            if not vc:
                # Create a new VC if it doesn't exist
                vc = VCRegistrations.objects.create(
                    name=partner_name,
                    email=partner_email,
                    mobile=partner_mobile,
                    registration_id='VCRG-' + str(uuid.uuid4())[:4].upper(),  # Generate unique registration ID
                    status='pending'  # Set default status
                )

            # Check if startup exists based on name (case insensitive)
            startup = StartUpRegistrations.objects.filter(name__iexact=startup_name).first()

            if not startup:
                # Create a new startup if it doesn't exist
                startup = StartUpRegistrations.objects.create(
                    name=startup_name,
                    email=startup_email,
                    mobile=startup_mobile,
                    registration_id='SURG-' + str(uuid.uuid4())[:4].upper(),  # Generate unique registration ID
                    status='pending'  # Set default status
                )

            # Create meeting request using VC and startup information
            meeting_request = MeetingRequests.objects.create(
                start_up=startup,
                vc=vc,
                message=f"Meeting scheduled for {startup_name} with {partner_name}",
                status='scheduled',  # Set status as 'scheduled'
                meeting_type='offline',  # Set meeting type as 'offline'
                meeting_location=location,  # Set meeting location
                meeting_date=timezone.now().date(),  # Set meeting date as today's date
                meeting_time=meeting_time,  # Set meeting time
                next_level=next_level,
            )

            print(f"Meeting request created for {startup_name} with VC {partner_name}")

    print("Meeting requests created successfully!")

# Usage:
# Call create_meeting_requests_from_tsv function and pass the file path of your TSV file
# For example:
create_meeting_requests_from_tsv('/Users/vj/itnt/iTNT-Portal/ldevcatalyst/scripts/import_data/vc/vc_T.tsv')
