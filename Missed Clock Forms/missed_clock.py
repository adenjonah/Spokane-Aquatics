import json
from datetime import datetime

# Load the JSON data from the file
with open('forms.json', 'r') as file:
    data = json.load(file)

# Function to parse the date string with multiple formats
def parse_date(date_str):
    formats = [
        "%a %b %d %Y %H:%M:%S GMT%z (Pacific Daylight Time)",
        "%a %b %d %Y %H:%M:%S GMT%z (PDT)"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%B %d, %Y")
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized: {date_str}")

# Extract and format the relevant information
shifts_by_name = {}
for entry in data:
    user = entry["user"]
    answers = entry["answers"]
    
    full_name = f'{user["first_name"]} {user["last_name"]}'
    date_str = answers["44583_qiPt"]
    print(f"Parsing date: {date_str}")  # Debug statement
    date = parse_date(date_str)
    start_time = answers["44584_NCOL"]
    end_time = answers["44585_wmis"]
    notes = answers.get("45798_TEjE", "No notes")
    
    hours_str = f"{start_time} to {end_time}"  # Always use the input times directly
    
    shift_details = f"{date}, {hours_str}, Notes: {notes}"
    
    if full_name not in shifts_by_name:
        shifts_by_name[full_name] = []
    
    shifts_by_name[full_name].append(shift_details)
    print(f"Added shift for {full_name}: {shift_details}")  # Debug statement

# Write the results to a new text file
with open('output.txt', 'w') as output_file:
    for name, shifts in shifts_by_name.items():
        output_file.write(f"{name}:\n")
        for shift in shifts:
            output_file.write(f"  - {shift}\n")
        output_file.write("\n")

print("Output written to output.txt")
