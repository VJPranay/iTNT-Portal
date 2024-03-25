import csv
from django.utils import timezone
from profiles.models import VC, StartUp
from meetings.models import MeetingRequests
import uuid

def create_meeting_requests_from_tsv(file_path):
    with open(file_path, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')  # Assuming TSV file format
        next(reader)  # Skip the header row if it exists
        for row_number, row in enumerate(reader, start=1):
            if len(row) >= 10:  # Check if the row has at least 10 columns
                try:
                    # Unpack values from the row
                    firm_name, partner_name, partner_email, partner_mobile, startup_name, startup_email, startup_mobile, date, time, next_level_str = row[:10]

                    # Convert 'Yes' to True, else False for next_level
                    next_level = next_level_str.strip().lower() == 'yes'

                    # Split time into start_time and end_time
                    start_time_str = time.split('(')[1].split('-')[0].strip()  # Extract "12.00pm" from "Suit 1 (12.00pm-12.15pm)"
                    start_time = timezone.datetime.strptime(start_time_str, '%I.%M%p').time()  # Parse start time

                    # Parse meeting date from string
                    meeting_date = timezone.datetime.strptime(date, '%b %d, %Y').date()

                    # Check if VC exists based on email (case insensitive)
                    vc = VC.objects.filter(email__iexact=partner_email).first()

                    if not vc:
                        # Create a new VC if it doesn't exist
                        vc = VC.objects.create(
                            firm_name=firm_name,
                            partner_name=partner_name,
                            email=partner_email,
                            mobile=partner_mobile,
                        )

                    # Check if startup exists based on name (case insensitive)
                    startup = StartUp.objects.filter(name__iexact=startup_name).first()

                    if not startup:
                        # Create a new startup if it doesn't exist
                        startup = StartUp.objects.create(
                            name=startup_name,
                            email=startup_email,
                            mobile=startup_mobile,
                        )

                    # Create meeting request using VC and startup information
                    meeting_request = MeetingRequests.objects.create(
                        start_up=startup,
                        vc=vc,
                        message=f"Meeting scheduled for {startup_name} with {partner_name}",
                        status='scheduled',  # Set status as 'scheduled'
                        meeting_type='offline',  # Set meeting type as 'offline'
                        meeting_location='Suit',  # Set meeting location (you can modify this as needed)
                        meeting_date=meeting_date,  # Set meeting date
                        meeting_time=start_time,  # Set meeting start time
                        next_level=next_level,
                    )

                    print(f"Meeting request created for {startup_name} with VC {partner_name}")
                except ValueError as e:
                    print(f"Error in row {row_number}: {row} - {e}")
                    continue
            else:
                print(f"Invalid row format in row {row_number}: {row}")

    print("Meeting requests created successfully!")


create_meeting_requests_from_tsv('/Users/vj/itnt/iTNT-Portal/ldevcatalyst/scripts/import_data/vc/vc_T.tsv')
