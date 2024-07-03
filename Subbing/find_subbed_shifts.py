import json
from datetime import datetime
from collections import defaultdict
from re import S

# List of specific names to check in "last name, first name" format
specific_names_case = [
    "Aden, Jonah", "Berg, Lauren", "Baldwin, Mia", "Singleton, Grant", "Triebe, Shaelin",
    "LeMay, Shaylee", "Lockhart, Grace", "Houghton, Emily", "Allen, Olivia", "Hernandez-Perez, Natalie",
    "Adeniran, Chloe", "Dunlap, Haley", "Lollis, Olivia", "Ries, Katie", "Hrycenko, Krista",
    "Corrales, Raul", "Corrales, Aiyana", "Hanson, Cecilia", "Goettshe, Olivia", "Arndt, London",
    "Wallace, McKenna", "Sterger, Taylor", "Smith, Cooper", "Adams, Ella", "Thompson, Rowan",
    "bleam, bethany", "Caprye, Eliana", "Caprye, Joelle", "Blankenagel, Caitin", "Allen, Rylan",
    "Cummins, Journey", "Ramirez, Alora", "Carter, Kendall", "Asbjornsen, Elliot"
]

specific_names = [s.lower() for s in specific_names_case]

# Mapping of location IDs to names
location_map = {
    18932: "Liberty",
    18927: "Witter",
    18929: "Comstock",
    18930: "Hillyard",
    18928: "Cannon"
}

# Load the JSON data from the file
with open('input.json', 'r') as file:
    data = json.load(file)

# Function to extract relevant information and format dates/times
def extract_shadle_primary_shifts(data):
    results = defaultdict(list)
    
    text_to_avoid = ["manager meeting", "manger meeting"]
    
    for shift in data:
        user_name_for_shift = shift.get("user_name_for_shift")
        location_id = shift["location_id"]
        position_id = shift["position_id"]
        notes = shift["notes"]
        
        if user_name_for_shift and user_name_for_shift.lower() in specific_names and location_id != 18931 and location_id in location_map and position_id != 28199:
            skip_shift = False
            if notes:
                for text in text_to_avoid:
                    if text in notes.lower():
                        skip_shift = True
                        break
            
            if skip_shift:
                continue
            
            start_dt = datetime.fromisoformat(shift["start_time"])
            end_dt = datetime.fromisoformat(shift["end_time"])
            date = start_dt.strftime("%B %d, %Y")
            start_time = start_dt.strftime("%I:%M %p")
            end_time = end_dt.strftime("%I:%M %p")
            
            results[date].append({
                "name": ' '.join(user_name_for_shift.split(', ')[::-1]),
                "start_time": start_time,
                "end_time": end_time,
                "location": location_map[location_id],
                "notes": shift.get("notes")
            })
    return results

# Extract the relevant data
shadle_primary_info = extract_shadle_primary_shifts(data)

# Week ranges
weeks = {
    "week 1": ("June 17, 2024", "June 23, 2024"),
    "week 2": ("June 24, 2024", "June 30, 2024"),
    "week 3": ("July 1, 2024", "July 7, 2024"),
}

def write_shifts_to_file(shadle_primary_info, filename, start_date, end_date, week):
    shift_count = 0
    start_dt = datetime.strptime(start_date, "%B %d, %Y")
    end_dt = datetime.strptime(end_date, "%B %d, %Y")
    
    with open(filename, 'w') as output_file:
        output_file.write(f"Shadle Sub Shifts at other pools for {week} ({start_date} to {end_date})\n\n")
        for date, shifts in sorted(shadle_primary_info.items()):
            current_date = datetime.strptime(date, "%B %d, %Y")
            if start_dt <= current_date <= end_dt:
                output_file.write(f"{date}\n")
                for shift in shifts:
                    notes = shift.get('notes')
                    shift_count += 1
                    output_file.write(f"    {shift['name']}")
                    output_file.write(f" subbed from {shift['start_time']} to")
                    output_file.write(f" {shift['end_time']} at ")
                    output_file.write(f"{shift['location']}")
                    if notes:
                        output_file.write(f" for {shift['notes']}")
                    output_file.write("\n\n")
        output_file.write(f"\nTotal Shifts: {shift_count}\n")

# Write shifts for each week
for week, (start_date, end_date) in weeks.items():
    write_shifts_to_file(shadle_primary_info, f"{week}.txt", start_date, end_date, week)