import json
from datetime import datetime
from collections import defaultdict

# List of specific names to check in "last name, first name" format
specific_names = [
    "Aden, Jonah", "Berg, Lauren", "Baldwin, Mia", "Singleton, Grant", "Triebe, Shaelin",
    "LeMay, Shaylee", "Lockhart, Grace", "Houghton, Emily", "Allen, Olivia", "Hernandez-Perez, Natalie",
    "Adeniran, Chloe", "Dunlap, Haley", "Lollis, Olivia", "Ries, Katie", "Hrycenko, Krista",
    "Corrales, Raul", "Corrales, Aiyana", "Hansen, Cecilia", "Goettshe, Olivia", "Arndt, London",
    "Wallace, McKenna", "Sterger, Taylor", "Smith, Cooper", "Adams, Ella", "Thompson, Rowan",
    "Bleam, Bethany", "Caprye, Eliana", "Caprye, Joelle", "Blankenagel, Caitin", "Allen, Rylan",
    "Cummins, Journey", "Ramirez, Alora", "Carter, Kendall", "Asbjornsen, Elliot"
]

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
    for shift in data:
        user_name_for_shift = shift.get("user_name_for_shift")
        location_id = shift["location_id"]
        if user_name_for_shift and user_name_for_shift in specific_names and location_id != 18931 and location_id in location_map:
            start_dt = datetime.fromisoformat(shift["start_time"])
            end_dt = datetime.fromisoformat(shift["end_time"])
            date = start_dt.strftime("%B %d, %Y")
            start_time = start_dt.strftime("%I:%M %p")
            end_time = end_dt.strftime("%I:%M %p")
            results[date].append({
                "name": user_name_for_shift,
                "start_time": start_time,
                "end_time": end_time,
                "location": location_map[location_id],
                "notes": shift.get("notes")
            })
    return results

# Extract the relevant data
shadle_primary_info = extract_shadle_primary_shifts(data)

# Write the results to a text file grouped by date
with open('week2_subs.txt', 'w') as output_file:
    for date, shifts in sorted(shadle_primary_info.items()):
        output_file.write(f"Date: {date}\n")
        for shift in shifts:
            output_file.write(f"  Name: {shift['name']}\n")
            output_file.write(f"  Start Time: {shift['start_time']}\n")
            output_file.write(f"  End Time: {shift['end_time']}\n")
            output_file.write(f"  Location: {shift['location']}\n")
            if shift['notes']:
                output_file.write(f"  Notes: {shift['notes']}\n")
            output_file.write("\n")
