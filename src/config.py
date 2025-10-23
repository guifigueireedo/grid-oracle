import os
from dotenv import load_dotenv

#carrega variaveis do env
load_dotenv()

#=== SECRET KEYS ===
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
HF_HUB_TOKEN = os.environ.get("HF_HUB_TOKEN")

#=== REPO IDS ===
HF_MODEL_REPO_ID = os.environ.get("HF_MODEL_REPO_ID")
HF_DATASET_REPO_ID = os.environ.get("HF_DATASET_REPO_ID")

#=== ARQUIVOS SALVOS NO HUB ===
TRAINING_DATASET_FILENAME = "f1_training_dataset.parquet"
POSITION_MODEL_FILENAME = "position_model.joblib"
DNF_MODEL_FILENAME = "dnf_model.joblib"
MODEL_METADATA_FILENAME = "model_metadata.json"

#=== CONSTANTES PROJETO ===
ERGAST_API_URL = "http://ergast.com/api/f1"
HTTP_USER_AGENT = "GridOracle/1.0 (https://github.com/guifigueireedo/grid-oracle)"

#=== CONSTANTES COLETA ===
DATA_START_YEAR = 2014
DATA_END_YEAR = 2024

DNF_STATUS_LIST = [
"Accident", "Collision", "Engine", "Gearbox", "Transmission",
    "Clutch", "Hydraulics", "Electrical", "Suspension", "Brakes",
    "Puncture", "Driveshaft", "Retired", "Fuel pump", "Fuel leak",
    "Overheating", "Wheel", "Spun off", "Radiator", "Electronics",
    "Mechanical", "Tyre", "Driver error", "Collision damage",
    "Power loss", "Water leak", "Damage", "Out of fuel", "Disqualified",
    "Withdrew", "Safety", "Driver sick"
]

#if __name__ == "__main__":
#    print("CONFIGS")
#    print(f"GROQ: {'ON' if GROQ_API_KEY else 'OFF'}")
#    print(f"OPENWEATHER: {'ON' if OPENWEATHER_API_KEY else 'OFF'}")
#    print(f"HF_HUB_TOKEN: {'ON' if HF_HUB_TOKEN else 'OFF'}")
#    print(f"HF Model Repo: {HF_MODEL_REPO_ID}")
#    print(f"HF Dataset Repo: {HF_DATASET_REPO_ID}")
#    print(f"Dados de: {DATA_START_YEAR} a {DATA_END_YEAR}")