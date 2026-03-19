import os #imports os to navigate folders and read environment variables
import json #imports json to parse files and minify data
import requests #imports requests to make api calls to openf1
from groq import Groq #imports the groq client for the llama model
from dotenv import load_dotenv #imports load_dotenv to read the .env file securely
from datetime import datetime, timezone #imports datetime and timezone for time handling

def load_text_folder(folder_path): #defines function to process all txt summaries
    combined_text = "" #initializes an empty string for the summaries
    try: #starts error handling for folder reading
        #sorted() ensures 2023 is read before 2024, maintaining chronological order
        for filename in sorted(os.listdir(folder_path)): #loops through files in folder
            if filename.endswith(".txt"): #checks if it is a text file
                filepath = os.path.join(folder_path, filename) #builds full path
                with open(filepath, "r", encoding="utf-8") as file: #opens file safely
                    combined_text += f"\n--- {filename} ---\n" #adds a header for ai context
                    combined_text += file.read() + "\n" #appends the text content
        return combined_text #returns the massive string with all summaries
    except Exception as e: #catches errors
        print(f"debug: failed to load text folder {folder_path} - {e}") #prints error
        return "" #returns empty string as fallback

def distill_current_data(folder_path): #defines function to process current data json files into a concise format for the ai
    distilled_summary = "" #empty string to get filled with the distilled data
    try: #error handling for folder reading and json parsing
        for filename in os.listdir(folder_path): #iterates through files in the current data folder
            if filename.endswith(".json"): #checks if it is a json file
                filepath = os.path.join(folder_path, filename) #builds the full path to the json file
                with open(filepath, "r", encoding="utf-8") as file: #opens the json file safely
                    data = json.load(file) #parses the json data into a dictionary
                    
                drivers = {d['driver_number']: d['full_name'] for d in data.get('drivers', [])} #map driver numbers to names for easy reference in the summary
                gp_name = data.get('meeting', {}).get('meeting_name', filename) #same for gp name, with fallback to filename if not found in json
                
                distilled_summary += f"\n--- {gp_name} ---\n" #adds a header for the ai context with the gp name
                
                active_drivers_list = ", ".join([d['full_name'] for d in data.get('drivers', [])])
                distilled_summary += f"\n[ACTIVE 2026 GRID FOR THIS EVENT]: {active_drivers_list}\n"
                
                for session in data.get('sessions', []): #iterates through the sessions in the json, which could be practice, qualifying
                    s_key = session['session_key'] #gets the session key to match with results
                    s_name = session['session_name'] #gets the session name for the summary header
                    
                    results = [r for r in data.get('session_results', []) if r['session_key'] == s_key] #gets only the results that match the current session key
                    if not results: continue #skips if there are no results for this session
                    
                    distilled_summary += f"[{s_name}]: " #adds the session name as a header for the results
                    for r in sorted(results, key=lambda x: x.get('position') or 99): #sorts results by position, putting DNFs at the end
                        name = drivers.get(r['driver_number'], f"#{r['driver_number']}") #map driver number to name, with fallback to number if not found
                        pos = f"P{r['position']}" if r['position'] else "DNF" #formats position, showing DNF if there is no position
                        distilled_summary += f"{name}({pos},+{r['gap_to_leader']}s); " #adds the driver performance to the summary in a concise format
                    distilled_summary += "\n"            
                    
        return distilled_summary #returns the final summary
    except Exception as e: #catch errors
        print(f"debug: failed to distill folder {folder_path} - {e}") #prints error message
        return "" #returns empty string as fallback
    
def get_next_race_context(): # defines function to automatically find the next grand prix
    url = "https://api.openf1.org/v1/sessions?year=2026&session_name=Race" # sets the openf1 calendar endpoint for 2026 races
    try: # starts error handling for network request
        response = requests.get(url, timeout=10) # fetches the full 2026 calendar from openf1
        if response.status_code == 200: # checks if the api call was successful
            races = response.json() # parses the json response into a python list
            now = datetime.now(timezone.utc) # gets the exact current date and time in utc
            
            for race in races: # loops through every race in the calendar chronologically
                date_str = race.get("date_start") # extracts the start date string of the race
                if date_str: # ensures the date string actually exists
                    # converts the iso string to a timezone-aware python datetime object
                    race_time = datetime.fromisoformat(date_str.replace("Z", "+00:00")) 
                    
                    if race_time > now: # logically checks if the race date is in the future
                        country = race.get("country_name") # extracts the country name of the next race
                        circuit = race.get("circuit_short_name", "the circuit") # extracts the circuit name with a fallback
                        print(f"debug: next race dynamically identified as {country}...") # prints the finding to terminal
                        return f"{country} Grand Prix at {circuit}" # returns a clean, formatted string for the ai prompt
                        
        return "the upcoming 2026 race" # returns a generic fallback if loop finishes without future races
    except Exception as e: # catches any network or parsing failures
        print(f"debug: failed to fetch next race automatically - {e}") # prints the exact error
        return None #returns nothing if theres an error

def generate_race_prediction(): #defines the main function to generate the race prediction
    load_dotenv() #loads .env file to get the api key securely
    api_key = os.getenv("GROQ_API_KEY") #reads the groq api key
    
    if not api_key: #checks if the key is available
        print("debug: GROQ_API_KEY not found in .env.") #prints error if key is missing
        return #exits the function if there is no api key
        
    client = Groq(api_key=api_key) #initializes the groq client with the api key
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    backend_dir = os.path.dirname(script_dir)
    
    past_data_path = os.path.join(backend_dir, "data", "historical_resumes")
    current_data_path = os.path.join(backend_dir, "data", "current_data")
    
    past_data = load_text_folder(past_data_path) 
    current_data = distill_current_data(current_data_path)

    print("debug: detecting the next race for context injection...") # prints the dynamic detection step
    next_race = get_next_race_context()
    print(f"debug: next race: {next_race}") #prints the identified next race
        
    print("debug: building engineered prompts...") #debug message to indicate that the prompts are being built
    
    system_prompt = (
        f"""
        You are an elite Formula 1 race strategist and data analyst. Your task is to simulate a highly realistic, data-driven race outcome for the upcoming {next_race}.

        INSTRUCTIONS:
        1. CURRENT ACTIVE GRID ONLY: Use ONLY the exact 22 drivers listed in the provided 'current_data_2026'. Don't create drivers, the sum of the grid must be exactly 22.
        2. RECENT FORM OVER REPUTATION: You MUST heavily weight the 2026 data. If a top driver has multiple DNFs or bad performances, they will have a lower prediction. If a low/midfield driver is consistently finishing in the top 10, they will have a better prediction. Consider realistic variation on the data given and on reputation of the drivers/team.
        3. RELATIVE SUCCESS & POINTS ZONE: Points are only awarded from P1 to P10. You must evaluate performance relative to the team's tier. P7 is a disaster for a Top 5 team, but a massive success for teams with the worst cars like Aston Martin or Cadillac. Reflect this context in your analysis.
        4. REALISTIC DNF: A normal F1 race has 1 to 3 DNFs. Extreme anomalies (+6 DNFs) are exceptionally rare. Don't just assign DNFs based on the numbers of DNF's of last race. 
        5. DATA-GROUNDED REASONING: Your explanations MUST have a justified and different explanation for each driver. Generic phrases like "struggled with pace" and "consistent points" are banned. The final explanation must have 200 characters min.
        6. DNF FORMATTING: Do NOT assign a finishing position (P-number) to a driver who DNFs. Place all DNFs at the bottom of the classification.

        OUTPUT FORMAT:

        [RESULTS]
        P1 - Driver Name - Explanation.
        P2 - Driver Name - Explanation.
        ...
        P10 - Driver Name - Explanation (Inside the points).
        P11 - Driver Name - Explanation (Outside the points).
        ...
        DNF - Driver Name - Reason (e.g., Engine failure, Lap 1 collision).
        """
    )
    
    user_prompt = ( #defines the user prompt (specific data it needs to analyze in order to make the prediction)
        f"historical_data_summaries:\n{past_data}\n\n" 
        f"current_data_2026:\n{current_data}\n\n" 
    ) 
    
    print("debug: sending request to groq (llama-3.3-70b-versatile)...") #prints message before requesting the ai prediction
    
    try: #error handling for the ai request
        response = client.chat.completions.create( #requests to the groq client to create a specific chat
            model="llama-3.3-70b-versatile", #specifies the model to use for the prediction
            messages=[ #the messages for the chat, including the system prompt and user prompt
                {"role": "system", "content": system_prompt}, 
                {"role": "user", "content": user_prompt} 
            ], 
            temperature=0.6, #sets the creativity of the response, lower means more deterministic
            max_tokens=2500 #sets the maximum number of tokens in the response
        ) 
        
        prediction = response.choices[0].message.content #extracts the content of the ai response
        
        print("\n=== grid oracle: race prediction ===")
        print(prediction) #prints the ai prediction
        print("====================================") 

        return prediction #returns the prediction for frontend use
        
    except Exception as e: #catches errors in the ai request
        print(f"debug: ai request failed - {e}") #prints error message if the ai request fails

if __name__ == "__main__": #checks if the script is being run directly
    print("debug: starting grid oracle ml pipeline...") #debug message to indicate the start of the process
    generate_race_prediction() #calls the main function to generate