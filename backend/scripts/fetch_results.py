import json
import requests
import time
import os

# Set up the exact paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DATA_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "../../frontend/src/data/calendar.json"))

def patch_calendar_results():
    print("--- STARTING RESULTS PATCH ---")
    
    # 1. Load the existing calendar (to protect the AI predictions)
    with open(FRONTEND_DATA_PATH, 'r', encoding='utf-8') as f:
        calendar = json.load(f)

    base_url = "https://api.openf1.org/v1/"

    # 2. Iterate only through completed races
    for event in calendar:
        if event.get("status") == "completed":
            print(f"\n[DEBUG] Processing {event['name']}...")
            meeting_key = event["id"].replace("mk_", "") # Extract ID
            
            # Fetch sessions
            print(f"[DEBUG] Fetching sessions for meeting_key={meeting_key}...")
            response_s = requests.get(f"{base_url}sessions?meeting_key={meeting_key}")
            time.sleep(3) # Crucial sleep to avoid rate limiting
            response_s.raise_for_status()
            sessions = response_s.json()
            
            # Find the actual Race session
            race_session = next((s for s in sessions if s.get("session_name") == "Race"), None)
            if not race_session:
                print("[DEBUG] No Race session found, skipping.")
                continue
                
            session_key = race_session["session_key"]
            print(f"[DEBUG] Found Race session_key={session_key}")

            # Fetch Drivers
            print(f"[DEBUG] Fetching drivers...")
            response_d = requests.get(f"{base_url}drivers?session_key={session_key}")
            time.sleep(3)
            response_d.raise_for_status()
            drivers_map = {d["driver_number"]: d.get("full_name", str(d["driver_number"])) for d in response_d.json()}

            # Fetch Results
            print(f"[DEBUG] Fetching session results...")
            response_res = requests.get(f"{base_url}session_result?session_key={session_key}")
            time.sleep(3)
            response_res.raise_for_status()
            results_data = response_res.json()
            
            actual_results = []
            
            # Sort by position, treating null/None as 999 (DNFs at the bottom)
            results_data.sort(key=lambda x: x.get('position') or 999)

            for res in results_data:
                drv_num = res.get("driver_number")
                pos = res.get("position")
                if pos is None:
                    pos = "DNF"
                
                gap = res.get("gap_to_leader", "")
                if gap is not None and gap != "":
                    # If it's a number (like 3.4), add '+s'. If it's '+1 LAP', leave as string.
                    if isinstance(gap, (int, float)):
                        gap = f"+{gap}s"
                    else:
                        gap = str(gap)
                else:
                    gap = ""
                    
                actual_results.append({
                    "name": drivers_map.get(drv_num, f"Driver {drv_num}"),
                    "position": pos,
                    "gap": gap
                })
            
            # Overwrite the empty [] with the real data
            event["results"] = actual_results
            print(f"[DEBUG] Successfully added {len(actual_results)} drivers to {event['name']}.")

    # 3. Save the patched JSON back to the frontend
    with open(FRONTEND_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(calendar, f, indent=4)
        
    print("\n--- PATCH COMPLETE ---")

if __name__ == "__main__":
    patch_calendar_results()