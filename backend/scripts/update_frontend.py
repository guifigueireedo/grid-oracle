import requests
import json
import time
import os
import re
from datetime import datetime, timezone
from analyze_predictions import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DATA_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "../../frontend/src/data/calendar.json"))

def fetch_and_build_calendar():
    print("Fetching 2026 calendar from OpenF1...")
    base_url = "https://api.openf1.org/v1/"
    
    response_r = requests.get(f"{base_url}sessions?year=2026&session_name=Race")
    time.sleep(1)
    response_r.raise_for_status()
    races = response_r.json()

    now = datetime.now(timezone.utc)
    frontend_calendar = []
    found_next_race = False

    races.sort(key=lambda x: x.get("date_start", ""))

    for r in races:
        meeting_key = r.get("meeting_key")
        session_key = r.get("session_key")
        
        response_m = requests.get(f"{base_url}meetings?meeting_key={meeting_key}")
        time.sleep(1)
        response_m.raise_for_status()
        meeting = response_m.json()[0]

        country = r.get("country_name")
        meeting_name = meeting.get("meeting_name")
        date_str = r.get("date_start")
        race_time = datetime.fromisoformat(date_str.replace("Z", "+00:00")) if date_str else now

        event = {
            "id": f"mk_{meeting_key}",
            "name": meeting_name,
            "location": r.get("location", country),
            "date": race_time.strftime("%b %d, %Y"),
            "date_start_utc": date_str,
            "circuit_image": meeting.get("circuit_image", ""),
            "country_flag": meeting.get("country_flag", "")
        }

        if country in ["Bahrain", "Saudi Arabia"]:
            event["status"] = "cancelled"
            event["date"] = "Cancelled"

        elif race_time < now:
            event["status"] = "completed"
            print(f"Fetching actual results for {meeting_name}...")
            
            response_s = requests.get(f"{base_url}sessions?meeting_key={meeting_key}")
            time.sleep(1)
            sessions = response_s.json()
            race_session = next((s for s in sessions if s.get("session_name") == "Race"), None)
            
            actual_results = []
            if race_session:
                session_key = race_session["session_key"]
                
                print(f"[DEBUG] Fetching drivers for session_key={session_key}")
                response_d = requests.get(f"{base_url}drivers?session_key={session_key}")
                time.sleep(1)
                
                drivers_map = {}
                if response_d.status_code == 200:
                    for d in response_d.json():
                        drivers_map[d["driver_number"]] = d.get("full_name", f"Driver {d.get('driver_number')}")
                
                print(f"[DEBUG] Fetching results for session_key={session_key}")
                response_res = requests.get(f"{base_url}session_result?session_key={session_key}")
                time.sleep(1)
                
                if response_res.status_code == 200:
                    results_data = response_res.json()
                    results_data.sort(key=lambda x: x.get('position') or 999) 
                    
                    for res in results_data:
                        drv_num = res.get("driver_number")
                        pos = "DNF" if res.get("position") is None else res.get("position")
                        
                        gap = res.get("gap_to_leader", "")
                        if gap is not None and gap != "":
                            gap = f"+{gap}s" if isinstance(gap, (int, float)) else str(gap)
                        else:
                            gap = ""
                            
                        # Lean structure: only name, position, and gap
                        actual_results.append({
                            "name": drivers_map.get(drv_num, f"Driver {drv_num}"),
                            "position": pos,
                            "gap": gap
                        })
                        
            event["results"] = actual_results

        elif race_time >= now and not found_next_race:
            event["status"] = "next"
            found_next_race = True

            print(f"Triggering AI prediction for {meeting_name}...")
            ai_text = generate_race_prediction()

            predictions = []
            if ai_text:
                lines = ai_text.split("\n")
                for l in lines:
                    l = l.strip()
                    if (l.startswith('P') and l[1:2].isdigit()) or l.startswith('DNF'):
                        parts = l.split("-", 2)
                        if len(parts) >= 3:
                            pos_str = parts[0].strip()
                            raw_name = parts[1].strip()
                            explanation = parts[2].strip()

                            pos = 'DNF' if pos_str == 'DNF' else int(pos_str.replace('P', ''))
                            clean_name = re.sub(r'\s*\(\d+\)\s*', '', raw_name)

                            # Lean structure: only name, position, and explanation
                            predictions.append({
                                "name": clean_name,
                                "position": pos,
                                "explanation": explanation
                            })
            
            event["predictions"] = predictions

        else:
            event["status"] = "future"

        frontend_calendar.append(event)

    return frontend_calendar

if __name__ == "__main__":
    print("-- GRID ORACLE AUTOMATION STARTED --")
    calendar_data = fetch_and_build_calendar()

    os.makedirs(os.path.dirname(FRONTEND_DATA_PATH), exist_ok=True)
    with open(FRONTEND_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(calendar_data, f, indent=4)
    print("-- AUTOMATION COMPLETE --")