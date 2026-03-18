import requests
import time
import json
import os
from datetime import datetime, timezone

def fetch_latest_meeting_data(year):
    base_url = "https://api.openf1.org/v1/"
    all_data = {}

    response_m = requests.get(f"{base_url}meetings?year={year}")
    time.sleep(1)
    response_m.raise_for_status()
    meetings = response_m.json()

    now = datetime.now(timezone.utc)
    completed_meetings = []

    # 1. Filter out future races and pre-season testing
    for m in meetings:
        if m.get("meeting_name") == "Pre-Season Testing":
            continue
        date_end_str = m.get("date_end")
        if date_end_str:
            end_time = datetime.fromisoformat(date_end_str.replace("Z", "+00:00"))
            if end_time < now:
                completed_meetings.append(m)

    if not completed_meetings:
        print("No completed races found yet.")
        return None, None

    # 2. Grab the most recently completed meeting
    completed_meetings.sort(key=lambda x: x.get("date_end", ""))
    latest_meeting = completed_meetings[-1]
    
    meeting_name = latest_meeting.get("meeting_name")
    country_name = latest_meeting.get("country_name", "unknown").lower().replace(" ", "_")
    end_time = datetime.fromisoformat(latest_meeting.get("date_end").replace("Z", "+00:00"))
    
    # 3. THE WEEKEND CHECK: Did this race happen THIS past weekend?
    # If it's been more than 4 days since the race ended, it's an off-week.
    days_since_race = (now - end_time).days
    if days_since_race > 4:
        print(f"Off-weekend detected. The last race ({meeting_name}) ended {days_since_race} days ago. Going back to sleep.")
        return None, None

    print(f"Recent race detected: {meeting_name}. Fetching telemetry...")
    meeting_key = latest_meeting["meeting_key"]

    all_data["meeting"] = {
        "meeting_key": meeting_key,
        "circuit_image": latest_meeting.get("circuit_image"),
        "country_flag": latest_meeting.get("country_flag"),
        "country_name": latest_meeting.get("country_name"),
        "location": latest_meeting.get("location"),
        "year": latest_meeting.get("year"),
        "date_start": latest_meeting.get("date_start"),
        "date_end": latest_meeting.get("date_end"),
        "meeting_name": meeting_name
    }

    response_s = requests.get(f"{base_url}sessions?meeting_key={meeting_key}")
    time.sleep(3)
    response_s.raise_for_status()
    sessions = response_s.json()
    all_data["sessions"] = []

    response_d = requests.get(f"{base_url}drivers?meeting_key={meeting_key}")
    time.sleep(3)
    response_d.raise_for_status()
    drivers_list = response_d.json()
    drivers = []

    for d in drivers_list:
        drivers.append({
            "driver_number": d.get("driver_number"),
            "full_name": d.get("full_name"),
            "team_name": d.get("team_name"),
        })
    all_data["drivers"] = drivers

    all_data["session_results"] = []
    for s in sessions:
        session_key = s["session_key"]
        session_info = {
            "country_name": latest_meeting.get("country_name"),
            "location": latest_meeting.get("location"),
            "session_name": s.get("session_name"),
            "date_start": s.get("date_start"),
            "date_end": s.get("date_end"),
            "meeting_key": meeting_key,
            "session_key": session_key
        }
        all_data["sessions"].append(session_info)

        print(f"Fetching results for session {session_key} ({s.get('session_name')})")

        response_r = requests.get(f"{base_url}session_result?session_key={session_key}")
        time.sleep(3)
        response_r.raise_for_status()
        results = response_r.json()

        for r in results:
            result_entry = {
                "dnf": r.get("dnf"),
                "dns": r.get("dns"),
                "dsq": r.get("dsq"),
                "driver_number": r.get("driver_number"),
                "position": r.get("position"),
                "duration": r.get("duration"),
                "gap_to_leader": r.get("gap_to_leader"),
                "number_of_laps": r.get("number_of_laps"),
                "meeting_key": meeting_key,
                "session_key": session_key
            }
            # (Keeping your qualifying logic intact here if needed, omitted for brevity, just paste your quali block here)
            all_data["session_results"].append(result_entry)
            
    # Generate the dynamic filename (e.g., "2026_japan_gp.json")
    filename = f"{year}_{country_name}_gp_{meeting_key}.json"
    return all_data, filename

def save_to_json(data, filename):
    os.makedirs("current_data", exist_ok=True)
    filepath = os.path.join("current_data", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Successfully saved {filename}")

if __name__ == "__main__":
    year = 2026
    print("Checking for recent 2026 data...")
    recent_gp_data, filename = fetch_latest_meeting_data(year)

    if recent_gp_data and filename:
        save_to_json(recent_gp_data, filename)
    print("Process finished")