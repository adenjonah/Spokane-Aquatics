import json
from collections import defaultdict

# Sample JSON data
with open('employees.json', 'r') as file:
    data = json.load(file)

# Sample location map
location_map = {
    18931: "Shadle",
    18932: "Liberty",
    18927: "Witter",
    18929: "Comstock",
    18930: "Hillyard",
    18928: "A.M. Cannon"
}

def extract_primary_location_and_employee_details(data):
    primary_location_employees = defaultdict(list)
    
    for employee in data:
        # Extract primary location from the tool_tip
        tool_tip = employee["user_locations_html"]["tool_tip"]
        locations = tool_tip.split(',')
        
        primary_location_name = None
        for location in locations:
            if "(Primary)" in location:
                primary_location_name = location.replace("(Primary)", "").strip()
                break
        
        if primary_location_name:
            # Find the corresponding location ID
            primary_location_id = next((id for id, name in location_map.items() if name == primary_location_name), None)
            
            if primary_location_id is not None:
                # Add employee name and ID to the primary location
                full_name = f"{employee['first_name']} {employee['last_name']}"
                primary_location_employees[primary_location_id].append({"name": full_name, "id": employee["id"]})
    
    return dict(primary_location_employees)

result = extract_primary_location_and_employee_details(data)

# Export the result
output_file = 'primary_location_employees.json'
with open(output_file, 'w') as file:
    json.dump(result, file, indent=4)

print(f"Employee names and IDs by primary location have been exported to {output_file}")