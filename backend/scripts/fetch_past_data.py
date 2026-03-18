import requests #imports the requests library to handle https calls
import time     #provides sleep functionality and time-related utilities
import json     #imports the json library to parse and save data
import os       #imports the os library to handle file paths and directories

def fetch_past_sessions():                  #defines the function to get historical data
    base_url = "https://api.openf1.org/v1"  #sets the root for the openf1 api
    years_to_fetch = [2025]                 #defines a list with the target historical years
    historical_data = []                    #inicializates an empty list to store the collected data

    for year in years_to_fetch: #starts a loop through each year in target years
        print(f"fetching data for year {year}") #debug message for the current year

        try:    #starts an error handling block for the network request
            response_m = requests.get(f"{base_url}/meetings?year={year}")   #sends a get request to the api
            time.sleep(3)                                                   #pause between meetings request and processing
            response_m.raise_for_status()                                   #checks if the response has en arror status code and raise a exception status if so
            meetings = response_m.json()                                    #parses the successful json response into a python list

            for m in meetings: #loops through each race session found in the year requested
                meeting_key = m.get("meeting_key")                                          #extracts the unique id for the current race

                response_s = requests.get(f"{base_url}/sessions?meeting_key={meeting_key}") #requests session list for a given meeting
                time.sleep(3)
                response_s.raise_for_status()                                               #raises an error if session request failed
                sessions = response_s.json()                                                #parses the session response into Python data

                for s in sessions: #iterate through each session returned for the meeting
                    if s["session_name"] in ["Sprint Qualifying", "Sprint", "Qualifying", "Race"]:
                        print(f"fetching data for {s["session_name"]} of {m["meeting_name"]}")  #log which session is being processed
                        sk = s["session_key"]                                                   #extracts the unique session identifier

                        try:
                            response_st = requests.get(f"{base_url}/session_result?session_key={sk}")  #fetch standings for the specific session
                            time.sleep(3)                   #delay before requesting results to respect API limits
                            response_st.raise_for_status()  #check for HTTP errors on standings request
                            standings = response_st.json()  #convert standings response to Python object
                        except requests.exceptions.RequestException:
                            print(f"no results for session {sk}")
                            continue

                        session_info = {
                            "meeting": meeting_key,
                            "gp": m["meeting_name"],
                            "year": year,
                            "session": s["session_name"],
                            "standings": standings,
                        }

                        print(f"{s["session_name"]} of {m["meeting_name"]} saved to data/2025_data.json")   #confirm session info appended
                        historical_data.append(session_info)                                                #adds the cleaned session data to the main list
        
        except requests.exceptions.RequestException as e: #catches any network related problems
            print(f"error fetching data for {year}: {e}") #prints the error message on terminal
    
    return historical_data #returns the complete list of collected historical session data

def save_to_json(data, filename): #defines a function to save python data to a json file
    os.makedirs("data", exist_ok=True)          #ensure the 'data' directory exists before writing file
    filepath = os.path.join("data", filename)   #constructs the path where JSON will be saved

    with open(filepath, "w", encoding="utf-8") as file: #open target file for writing with utf-8 encoding
        json.dump(data, file, indent=4) #serialize python data to json with readable formatting
    
    print(f"successfully saved data to {filepath}") #inform user that save operation completed

if __name__ == "__main__": #checks if the script is bein run directly and not imported
    print("starting historical data fetching")  #log start of main script
    past_data = fetch_past_sessions()           #invoke fetch and store returned list

    if past_data: #verify that some sessions were collected
        save_to_json(past_data, "2025_data.json") #persist results to the JSON file
    else: #handle the case where no data was retrieved
        print(f"no data collected.") #output warning when nothing to save

    print("process finished") #indicate script completion