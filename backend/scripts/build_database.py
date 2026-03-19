import json
import os
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../frontend/src/data"))
CALENDAR_PATH = os.path.join(FRONTEND_DATA_DIR, "calendar.json")
DRIVERS_PATH = os.path.join(FRONTEND_DATA_DIR, "drivers.json")

def migrate_database():
    print("--- STARTING DATA MIGRATION ---")
    
    # 1. Fetch official driver data from OpenF1
    print("Fetching 2026 driver data from OpenF1...")
    # Using a known session from 2026 to get the grid
    response = requests.get("https://api.openf1.org/v1/drivers?session_key=11234") 
    api_drivers = response.json() if response.status_code == 200 else []

    drivers_dict = {}
    for d in api_drivers:
        full_name = d.get("full_name")
        if full_name:
            drivers_dict[full_name.lower()] = {
                "name": full_name,
                "driver_number": d.get("driver_number"),
                "team_name": d.get("team_name"),
                "team_colour": d.get("team_colour", "FFFFFF"),
                "headshot_url": d.get("headshot_url", "")
            }

    # 2. Clean up calendar.json
    with open(CALENDAR_PATH, 'r', encoding='utf-8') as f:
        calendar = json.load(f)

    for event in calendar:
        for list_type in ["results", "predictions"]:
            if list_type in event:
                for item in event[list_type]:
                    # Remove the bloat!
                    for key in ["team_name", "team_colour", "headshot_url", "country_code"]:
                        item.pop(key, None)

    # 3. Save both files
    with open(DRIVERS_PATH, 'w', encoding='utf-8') as f:
        json.dump(list(drivers_dict.values()), f, indent=4)

    with open(CALENDAR_PATH, 'w', encoding='utf-8') as f:
        json.dump(calendar, f, indent=4)
        
    print(f"Migration Complete! Saved {len(drivers_dict)} drivers to drivers.json.")
    print("Cleaned calendar.json successfully.")

if __name__ == "__main__":
    migrate_database()