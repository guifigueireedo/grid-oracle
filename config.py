from datetime import datetime
import os

#=== CONFIGURAÇÕES GERAIS ===
CURRENT_YEAR: int = datetime.now().year #ano atual
HISTORICAL_YEARS: int = 5 #anos históricos para análise

#=== CONFIGURAÇÕES DE CAMINHOS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #diretório base do projeto
CACHE_DIR = os.path.join(BASE_DIR, 'f1_cache') #pasta de cache
HISTORICAL_DATA_FILE = os.path.join(BASE_DIR, 'f1_historical_data_5y.parquet') #arquivo de dados históricos
PREDICTION_OUTPUT_FILE = os.path.join(BASE_DIR, 'final_predictions.json') #arquivo de saída de previsões

#=== CONFIGURAÇÕES DE AI ===
AI_MODEL_NAME: str = "llama-3.1-8b-instant" #modelo AI a ser utilizado