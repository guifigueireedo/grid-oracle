import fastf1 as ff1
import requests_cache
import pandas as pd
import requests
import time
import sys
import os
from datetime import datetime, timezone

#=== IMPORTAR CONFIGS ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src import config
except ImportError:
    import config

#=== CONFIGURAÇÃO FASTF1 ===
requests_cache.install_cache('f1_http_cache', backend='sqlite', expire_after=3600)

try:
    os.makedirs(config.FASTF1_CACHE_PATH, exist_ok=True) 
    ff1.Cache.enable_cache(config.FASTF1_CACHE_PATH)
    print(f"CACHE DO FASTF1 HABILITADO EM: {config.FASTF1_CACHE_PATH}")
except Exception as e:
    print(f"ERRO AO HABILITAR O CACHE DO FASTF1: {e}")
    print("VERIFIQUE AS PERMISSÕES DA PASTA")

#=== COLETA HISTÓRICA ===
def fetch_race_results(start_year: int, end_year: int) -> pd.DataFrame:
    print(f"▶️INICIANDO COLETA DE RESULTADOS (DE {start_year} A {end_year})")
    all_races_data = []

    for year in range(start_year, end_year + 1):
        print(f"    🔎BUSCANDO DADOS DA TEMPORADA {year}")
        try:
            schedule = ff1.get_event_schedule(year, include_testing=False) 
            
            if schedule.empty:
                print(f"    ⚠️AVISO: Calendário para {year} está vazio. Pulando.")
                continue
            
            required_cols = ['EventDate', 'Location', 'RoundNumber', 'EventName']
            if not all(col in schedule.columns for col in required_cols):
                print(f"    ⚠️AVISO: Calendário de {year} está faltando colunas essenciais. Pulando.")
                continue

            schedule = schedule.dropna(subset=required_cols) 
            
            now = datetime.now(timezone.utc).replace(tzinfo=None)

            for event in schedule.itertuples():
                event_date = getattr(event, 'EventDate', None)
                if event_date is None or event_date > now:
                    continue
                
                is_race_event = False
                for i in range(1, 6):
                    session_name = getattr(event, f'Session{i}', '')
                    if session_name == 'Race':
                        is_race_event = True
                        break
                
                if not is_race_event:
                    # print(f"    ℹ️ Pulando evento não-corrida: {event.EventName}")
                    continue

                try:
                    session = ff1.get_session(year, event.RoundNumber, 'R')
                    session.load(telemetry=False, weather=False, messages=False)

                    if session.results is None:
                        print(f"    ⚠️AVISO: SESSÃO 'R' {year} ROUND {event.RoundNumber} ({event.EventName}) NÃO TEM RESULTADOS")
                        continue

                    for driver_number, row in session.results.iterrows():
                        grid_pos = pd.to_numeric(row.get('GridPosition'), errors='coerce')
                        final_pos = pd.to_numeric(row.get('Position'), errors='coerce')

                        data_point = {
                            'season': year,
                            'round': event.RoundNumber,
                            'circuit_location': event.Location,
                            'date': event.EventDate.date(),
                            'driverId': row.get('DriverId', 'Unknown'),
                            'constructorId': row.get('TeamId', 'Unknown'),
                            'grid': int(pd.Series(grid_pos).fillna(0).iloc[0]),
                            'position': int(pd.Series(final_pos).fillna(99).iloc[0]),
                            'status': row.get('Status', 'Unknown'),
                            'points': float(pd.Series(row.get('Points')).fillna(0).iloc[0]),
                        }
                        all_races_data.append(data_point)
                    
                    print(f"    ✅COLETADO: {event.EventName}")

                except ff1.errors.SessionNotAvailableError:
                     print(f"    ⚠️AVISO: Sessão 'R' para {event.EventName} ({year} R{event.RoundNumber}) não disponível.")
                except Exception as e:
                    print(f"    ❌ERRO AO CARREGAR SESSÃO {year} ROUND {event.RoundNumber} ({event.EventName}): {e}")

                time.sleep(0.1)
            
        except Exception as e:
            print(f"    ❌ERRO AO PROCESSAR CALENDÁRIO DE {year}: {e}")

    print("    ✅COLETA DE RESULTADOS CONCLUÍDA")
    return pd.DataFrame(all_races_data)

#=== COLETA PARA PREVISÃO ===
def get_next_race_info() -> dict:
    print("⏭️BUSCANDO INFORMAÇÕES DA PRÓXIMA CORRIDA")
    try:
        current_year = datetime.now().year
        schedule = ff1.get_event_schedule(current_year, include_testing=False)
        
        if schedule.empty:
            print(f"    ⚠️AVISO: Calendário para {current_year} está vazio.")
            return None
        
        required_cols = ['EventDate', 'Location', 'RoundNumber', 'EventName']
        if not all(col in schedule.columns for col in required_cols):
            print(f"    ⚠️AVISO: Calendário de {current_year} está faltando colunas. Pulando.")
            return None
            
        schedule = schedule.dropna(subset=required_cols) 

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        future_races = schedule[schedule['EventDate'] > now].sort_values(by='EventDate')
        
        next_race_event = None
        for index, event_row in future_races.iterrows():
            is_race_event = False
            for i in range(1, 6):
                session_name = event_row.get(f'Session{i}', '')
                if session_name == 'Race':
                    is_race_event = True
                    break
            if is_race_event:
                next_race_event = event_row
                break

        if next_race_event is None:
            print("    ⚠️AVISO: TEMPORADA ATUAL TERMINOU OU NENHUMA CORRIDA FUTURA ENCONTRADA.")
            return None

        print(f"    ‼️PRÓXIMA CORRIDA ENCONTRADA: {next_race_event['EventName']} (ROUND {next_race_event['RoundNumber']})")
        
        return {
            'season': str(current_year), 
            'round': str(next_race_event['RoundNumber']),
            'location': next_race_event['Location'],
            'race_date_iso': next_race_event['EventDate'].isoformat(),
        }
    except Exception as e:
        print(f"    ❌ERRO AO BUSCAR A PRÓXIMA CORRIDA: {e}")
        return None
    
#=== COLETA DADOS DA QUALI ===
def fetch_qualifying_results(season: str, round_num: str) -> dict:
    print(f"🏁BUSCANDO GRID DE LARGADA PARA {season}, ROUND {round_num}...")
    try:
        session = ff1.get_session(int(season), int(round_num), 'Q')
        session.load(telemetry=False, weather=False, messages=False)

        if session.results is None:
            print("    ⚠️AVISO: RESULTADO DA QUALIFICAÇÃO AINDA NÃO DISPONÍVEIS")
            return {}

        grid_map = {}
        for driver_number, row in session.results.iterrows():
             pos = pd.to_numeric(row.get('Position'), errors='coerce')
             grid_map[row.get('DriverId', 'Unknown')] = int(pd.Series(pos).fillna(99).iloc[0])
        
        print("    ✅GRID DE LARGADA OBTIDO")
        return grid_map
        
    except ff1.errors.SessionNotAvailableError:
         print(f"    ⚠️AVISO: Sessão 'Q' para {season} R{round_num} não disponível.")
         return {}
    except Exception as e:
        print(f"    ❌ERRO AO COLETAR RESULTADOS DA QUALIFICAÇÃO: {e}")
        return {}

#=== PREVISÃO DO TEMPO ===
def get_weather_forecast(location: str) -> dict:
    print("☁️INICIANDO BUSCA DE PREVISÃO DO TEMPO")
    if not config.OPENWEATHER_API_KEY:
        print("    ⚠️AVISO: CHAVE DA API OPENWEATHER NÃO CONFIGURADA")
        return None
    
    print(f"    🌦️BUSCANDO PREVISÃO DO TEMPO PARA: {location}")
    url = "https://api.openweathermap.org/data/2.5/forecast"
    
    params = {
        'q': location,
        'appid': config.OPENWEATHER_API_KEY,
        'units': 'metric',
    }
    headers = {"User-Agent": config.HTTP_USER_AGENT}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        print("    ✅PREVISÃO DO TEMPO OBTIDA")
        return response.json()
    except Exception as e:
        print(f"    ❌ERRO AO OBTER PREVISÃO DO TEMPO: {e}")
        return None
    
#if __name__ == "__main__":
#    print("--- Iniciando Teste de Coleta (FastF1) ---")
#    
#    TEST_START_YEAR = 2023
#    TEST_END_YEAR = 2025
#
#    race_df = fetch_race_results(start_year=TEST_START_YEAR, end_year=TEST_END_YEAR)
#    
#    if not race_df.empty:
#        print("\n--- Amostra de Resultados de Corridas (FastF1) ---")
#        print(race_df.head())
#        print(f"\nShape do DataFrame: {race_df.shape}")
#        print("\nInfo do DataFrame:")
#        race_df.info()
#        
#        print("\n--- Verificando GP de São Paulo ---")
#        interlagos_2023 = race_df[(race_df['season'] == 2023) & (race_df['circuit_location'] == 'São Paulo')]
#        interlagos_2024 = race_df[(race_df['season'] == 2024) & (race_df['circuit_location'] == 'São Paulo')]
#        
#        print(f"Resultados de Interlagos 2023 encontrados: {not interlagos_2023.empty}")
#        if not interlagos_2023.empty:
#            print(interlagos_2023[['driverId', 'position', 'points']].head())
#            
#        print(f"Resultados de Interlagos 2024 encontrados: {not interlagos_2024.empty}")
#        if not interlagos_2024.empty:
#            print(interlagos_2024[['driverId', 'position', 'points']].head())
#            
#    else:
#        print("\nNenhum resultado de corrida encontrado no teste.")
#    
#    print("\n--- Teste de Próxima Corrida ---")
#    next_race = get_next_race_info()
#    
#    if next_race:
#        print(f"Dados da próxima corrida: {next_race}")
#        
#        grid = fetch_qualifying_results(next_race['season'], next_race['round'])
#        print(f"Grid (pode estar vazio): {grid}")
#        
#        weather = get_weather_forecast(next_race['location'])
#        if weather:
#            print(f"Previsão do tempo obtida (Cidade: {weather.get('city', {}).get('name')})")
#    elif not next_race:
#         print("Nenhuma próxima corrida encontrada para testar Grid/Clima.")
#
#    print("\n--- Teste de Coleta Concluído ---")