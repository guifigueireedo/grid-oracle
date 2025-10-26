from datetime import datetime
import fastf1 as ff1
import pandas as pd
import config
import os

HISTORICAL_DATA_FILE = 'f1_historical_data_5y.parquet' #arquivo de dados históricos

#=== CARREGAR DADOS HISTÓRICOS ===
def load_historical_data(years = 5):
    if os.path.exists(HISTORICAL_DATA_FILE): #verifica se o arquivo de dados históricos existe
        print(f"🔄️ CARREGANDO DADOS HISTÓRICOS DO CACHE: {HISTORICAL_DATA_FILE}")
        return pd.read_parquet(HISTORICAL_DATA_FILE)
    
    print("⚠️ CACHE NÃO ENCONTRADO. CARREGANDO DADOS HISTÓRICOS DA F1")
    current_year = datetime.now().year #ano atual
    all_data = [] #array para armazenar dados dos 5 anos

    for year in range(current_year - years + 1, current_year + 1):
        schedule = ff1.get_event_schedule(year) #obter calendário de eventos do ano
        for _, event in schedule.iterrows():
            if event['EventDate'] < pd.to_datetime(datetime.now()): #verifica se o evento já ocorreu
                try:
                    session = ff1.get_session(year, event.EventName, 'R') #obter sessão de corrida
                    session.load(telemetry=False, weather=False) #carregar dados da sessão sem telemetria e clima
                    results = session.results #obter resultados da corrida
                    results['Year'] = year #adicionar coluna do ano
                    results['CircuitName'] = event['Circuit']['circuitName'] #adicionar nome do circuito
                    all_data.append(results) #adicionar resultados ao array
                except Exception as e:
                    print(f"❌ ERRO AO CARREGAR DADOS PARA {event.EventName} {year}: {e}")
                
    full_df = pd.concat(all_data, ignore_index=True) #concatenar todos os dados em um único DataFrame | DataFrame é uma estrutura de dados tabular do pandas que facilita a manipulação e análise de dados
    full_df.to_parquet(HISTORICAL_DATA_FILE) #salvar dados históricos em arquivo parquet
    return full_df

#=== PEGAR DADOS DA TEMPORADA ATUAL ===
def get_season_data():
    current_year = datetime.now().year

    if os.path.exists(HISTORICAL_DATA_FILE): #verifica se o arquivo de dados históricos existe
        print(f"🔄️ CARREGANDO DADOS DA TEMPORADA ATUAL DO CACHE: {HISTORICAL_DATA_FILE}")
        all_data = pd.read_parquet(HISTORICAL_DATA_FILE) #carregar dados históricos do arquivo parquet
        season_data = all_data[all_data['Year'] == current_year] #filtrar dados para a temporada atual
        return season_data
    
    print("⚠️ CACHE NÃO ENCONTRADO. CARREGANDO DADOS DA TEMPORADA ATUAL DA F1")
    schedule = ff1.get_event_schedule(current_year) #obter calendário de eventos do ano
    all_data = [] #array para armazenar dados da temporada atual

    for _, event in schedule.iterrows():
        if event['EventDate'] < pd.to_datetime(datetime.now()): #verifica se o evento já ocorreu
            try:
                session = ff1.get_session(current_year, event.EventName, 'R') #obter sessão de corrida
                session.load(telemetry=False, weather=False) #carregar dados da sessão sem telemetria e clima
                results = session.results #obter resultados da corrida
                results['Year'] = current_year #adicionar coluna do ano
                results['CircuitName'] = event['Circuit']['circuitName'] #adicionar nome do circuito
                all_data.append(results) #adicionar resultados ao array
            except Exception as e:
                print(f"❌ ERRO AO CARREGAR DADOS PARA {event.EventName} {current_year}: {e}")

    season_df = pd.concat(all_data, ignore_index=True) #concatenar todos os dados em um único DataFrame
    season_df.to_parquet(HISTORICAL_DATA_FILE) #salvar dados da temporada atual em arquivo parquet
    return season_df