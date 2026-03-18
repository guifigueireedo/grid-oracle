import requests
import time
import json
import os

def fetch_drivers(): #defines a function to fetch driver data for all meetings and sessions
    base_url = "https://api.openf1.org/v1/" #base URL for the api endpoint to fetch driver data
    drivers_data = [] #initialize an empty list to hold driver data

    response_m = requests.get(f"{base_url}meetings?year=2025")
    time.sleep(3) #pause for 3 seconds to respect API rate limits
    response_m.raise_for_status() #raise an exception if the response is an error
    meetings = response_m.json() #parse the response as JSON to get the list of meetings
    meeting_keys = {m["meeting_key"] for m in meetings} #extracts unique meeting keys from the meetings data

    meeting_keys_set = set(meeting_keys)
    last_meeting = list(meeting_keys_set)[-1]

    response_se = requests.get(f"{base_url}sessions?meeting_key={last_meeting}")
    time.sleep(3)
    response_se.raise_for_status()
    sessions = response_se.json()
    session_keys = {s["session_key"] for s in sessions}

    session_keys_set = set(session_keys)
    last_session = list(session_keys_set)[-1]

    response_st = requests.get(f"{base_url}championship_drivers?session_key={last_session}")
    time.sleep(3)
    response_st.raise_for_status()
    standings = response_st.json()
    driver_numbers = {d["driver_number"] for d in standings}

    for dn in driver_numbers: #iterate over each unique driver number to fetch their data

        for mk in meeting_keys: #iterate over each unique meeting key to fetch data for the current driver at that meeting

            try: #attempt to fetch driver data for the current driver and meeting combination
                response = requests.get(f"{base_url}drivers?meeting_key={mk}&driver_number={dn}")   #request driver data from the open f1 api
                time.sleep(3)                                                                       #pause for 3 seconds
                response.raise_for_status()                                                         #raise an exception if the response is an error
                data = response.json()                                                              #save the response in json format
                if data: #check if the response contains data before appending to the list
                    driver_info = data [0]

                    filtered_driver = {
                        "driver_number": driver_info.get("driver_number"),
                        "full_name": driver_info.get("full_name"),
                        "team_name": driver_info.get("team_name")
                    }

                    drivers_data.append(filtered_driver)    #appends to the list of driver data
                    print(f"fetched data for driver {dn}")  #debug
                    break                                   #stop iterating for this driver
            except requests.RequestException as e: #throws an exception if there is error
                print(f"error fetching data for driver {dn} at meeting {mk}: {e}") #debug

    return drivers_data #returns the list of driver data collected

def save_to_json(data, filename): #defines a function to save python data to a json file
    os.makedirs("data", exist_ok=True)          #ensure the 'data' directory exists before writing file
    filepath = os.path.join("data", filename)   #constructs the path where JSON will be saved

    with open(filepath, "w", encoding="utf-8") as file: #open target file for writing with utf-8 encoding
        json.dump(data, file, indent=4) #serialize python data to json with readable formatting
    
    print(f"successfully saved data to {filepath}") #inform user that save operation completed

if __name__ == "__main__": #checks if the script is bein run directly and not imported
    print("starting historical drivers data fetching")  #log start of main script
    past_data = fetch_drivers()                         #invoke fetch and store returned list

    if past_data: #verify that some sessions were collected
        save_to_json(past_data, "2026_drivers.json") #persist results to the JSON file
    else: #handle the case where no data was retrieved
        print(f"no data collected.") #output warning when nothing to save

    print("process finished") #indicate script completion