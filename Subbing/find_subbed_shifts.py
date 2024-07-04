import json
from datetime import datetime
from collections import defaultdict
import pandas as pd
import os

# Load primary location employees data
with open('primary_location_employees.json', 'r') as file:
    primary_location_employees = json.load(file)

# Load shifts data
with open('input.json', 'r') as file:
    data = json.load(file)

# Load location map
location_map = {
    18931: "Shadle",
    18932: "Liberty",
    18927: "Witter",
    18929: "Comstock",
    18930: "Hillyard",
    18928: "A.M. Cannon"
}

# Week ranges
weeks = {
    "week 1": ("June 17, 2024", "June 23, 2024"),
    "week 2": ("June 24, 2024", "June 30, 2024"),
    "week 3": ("July 1, 2024", "July 7, 2024"),
}

text_to_avoid = ["inservice", "manager meeting", "manger meeting"]

# Define the directory for output files
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def get_primary_location(user_id, primary_location_employees):
    for primary_location_id, employees in primary_location_employees.items():
        for employee in employees:
            if employee['id'] == user_id:
                return primary_location_id
    return None

def filter_shifts(data, primary_location_employees):
    filtered_shifts = []
    for shift in data:
        user_id = shift.get("user_id")
        if user_id is None:
            continue
        primary_location_id = get_primary_location(user_id, primary_location_employees)
        if primary_location_id is None:
            continue
        
        # Skip shifts at the employee's primary location
        if primary_location_id == str(shift["location_id"]):
            continue
        
        # Skip shifts with position_id 28199
        if shift["position_id"] == 28199:
            continue
        
        if shift["user_id"] in [203215, 227761, 203210, 203536]:
            continue
        
        notes = shift.get("notes")
        if notes:
            notes = notes.lower()
            if any(text in notes for text in text_to_avoid):
                continue
        
        shift['primary_location_id'] = primary_location_id
        filtered_shifts.append(shift)
    return filtered_shifts

def group_shifts_by_primary_pool(filtered_shifts):
    grouped_shifts = defaultdict(lambda: defaultdict(list))
    for shift in filtered_shifts:
        primary_location_id = shift["primary_location_id"]
        primary_location_name = location_map.get(int(primary_location_id), "Unknown")
        if primary_location_name == "Unknown":
            print(f"Warning: Unknown primary location ID {primary_location_id}")
        start_dt = datetime.fromisoformat(shift["start_time"])
        date = start_dt.strftime("%B %d, %Y")
        grouped_shifts[primary_location_name][date].append(shift)
    return grouped_shifts

def write_shifts_to_file(grouped_shifts, weeks):
    summary = defaultdict(lambda: defaultdict(int))
    
    for pool, dates in grouped_shifts.items():
        filename = os.path.join(output_dir, f"{pool}_subs.txt")
        with open(filename, 'w') as output_file:
            for week, (start_date, end_date) in weeks.items():
                output_file.write(f"{week.upper()}: {pool} Sub Shifts ({start_date} to {end_date})\n\n")
                start_dt = datetime.strptime(start_date, "%B %d, %Y")
                end_dt = datetime.strptime(end_date, "%B %d, %Y")
                shift_count = 0
                
                for date, shifts in sorted(dates.items()):
                    current_date = datetime.strptime(date, "%B %d, %Y")
                    if start_dt <= current_date <= end_dt:
                        output_file.write(f"{date}\n")
                        for shift in shifts:
                            shift_count += 1
                            user_name = ' '.join(shift["user_name_for_shift"].split(', ')[::-1])
                            start_time = datetime.fromisoformat(shift["start_time"]).strftime("%I:%M %p")
                            end_time = datetime.fromisoformat(shift["end_time"]).strftime("%I:%M %p")
                            notes = shift.get("notes", "")
                            sub_location_name = location_map.get(shift["location_id"], "Unknown")
                            output_file.write(f"    {user_name} subbed from {start_time} to {end_time} at {sub_location_name}")
                            if notes:
                                output_file.write(f" for {notes}")
                            output_file.write(f"\n")
                        output_file.write("\n")
                
                output_file.write(f"Total Shifts: {shift_count}\n\n\n\n\n")
                summary[pool][week] = shift_count
    
    return summary

def save_summary_to_txt(summary, weeks):
    # Convert the summary dictionary to a DataFrame and transpose it
    df = pd.DataFrame(summary).T

    # Calculate the total number of shifts per pool (row-wise)
    df["Total"] = df.sum(axis=1)

    # Calculate the total number of shifts per week (column-wise)
    df.loc["Total"] = df.sum()

    # Save the DataFrame to a text file with formatting
    with open(os.path.join(output_dir, "Summary.txt"), "w") as file:
        file.write(df.to_string())

filtered_shifts = filter_shifts(data, primary_location_employees)
with open(os.path.join(output_dir, 'Subbed_Shifts.json'), 'w') as file:
    json.dump(filtered_shifts, file, indent=4)

grouped_shifts = group_shifts_by_primary_pool(filtered_shifts)
summary = write_shifts_to_file(grouped_shifts, weeks)
save_summary_to_txt(summary, weeks)

print("Processing complete. Check the output files for results.")