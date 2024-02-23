import csv
from datarepo.models import State, District

def import_data_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        current_state = None
        for row in reader:
            state_name, district_name = row
            if current_state is None or current_state.name != state_name:
                current_state, _ = State.objects.get_or_create(name=state_name)
            District.objects.create(state=current_state, name=district_name)

# Replace 'file_path' with the path to your CSV file
file_path = '/opt/portal/iTNT-Portal/ldevcatalyst/scripts/import_data/disricts_states.csv'
import_data_from_csv(file_path)
