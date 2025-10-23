import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from src import config
except ImportError:
    import config

#=== TRATAMENTO INICIAL E CONVERSÕES ===
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    print("⚙️INICIANDO PRÉ-PROCESSAMENTO")

    processed_df = df.copy()

    processed_df['date'] = pd.to_datetime(processed_df['date'])

    processed_df['is_dnf'] = processed_df['status'].apply(
        lambda x: 1 if x in config.DNF_STATUS_LIST else 0
    )

    processed_df['grid'] = processed_df['grid'].replace(0, 21)

    processed_df['position'] = pd.to_numeric(processed_df['position'], errors='coerce')
    processed_df['grid'] = pd.to_numeric(processed_df['grid'], errors='coerce')

    processed_df.dropna(subset=['position'], inplace=True)
    processed_df['position'] = processed_df['position'].astype(int)

    print("    ✅PRÉ-PROCESSAMENTO CONCLUÍDO")
    return processed_df

#=== CALCULAR FORMA RECENTE ===
def calculate_rolling_features(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    print(f"📈CALCULANDO FORMA RECENTE (JANELA DE {window} CORRIDAS)")

    df_sorted = df.sort_values(by=['date', 'round']).copy()

    df_sorted['driver_recent_points'] = df_sorted.groupby('driverId')['points'].transform(
        lambda x: x.shift(1).rolling(window, min_periods=1).mean()
    )

    df_sorted['driver_recent_points'].fillna(0, inplace=True)

    team_points_per_race = df_sorted.groupby(['season', 'round', 'constructorId'])['points'].sum().reset_index()
    team_points_per_race = team_points_per_race.sort_values(by=['season', 'round'])

    team_points_per_race['constructor_recent_points'] = team_points_per_race.groupby('constructorId')['points'].transform(
        lambda x: x.shift(1).rolling(window, min_periods=1).mean()
    )
    team_points_per_race['constructor_recent_points'].fillna(0, inplace=True)

    df_sorted = pd.merge(
        df_sorted,
        team_points_per_race[['season', 'round', 'constructorId', 'constructor_recent_points']],
        on=['season', 'round', 'constructorId'],
        how='left'
    )

    df_sorted['constructor_recent_points'].fillna(0, inplace=True)

    print("    ✅FORMAS RECENTES CALCULADAS")
    return df_sorted

#=== CALCULA DESEMPENHO POR CIRCUITO ===
def calculate_track_features(df: pd.DataFrame) -> pd.DataFrame:
    print(f"🏟️CALCULANDO HISTÓRICO POR PISTA")
    
    df_sorted = df.sort_values(by=['date', 'round']).copy()

    df_sorted['driver_track_avg_pos'] = df_sorted.groupby(['driverId', 'circuit_location'])['position'].transform(
        lambda x: x.shift(1).expanding(min_periods=1).mean()
    )
    df_sorted['driver_track_dnf_rate'] = df_sorted.groupby(['driverId', 'circuit_location'])['is_dnf'].transform(
        lambda x: x.shift(1).expanding(min_periods=1).mean()
    )

    avg_dnf_rate = df_sorted['is_dnf'].mean() # Calcula a média geral de DNF
    df_sorted['driver_track_avg_pos'].fillna(15, inplace=True)
    df_sorted['driver_track_dnf_rate'].fillna(avg_dnf_rate, inplace=True)
    
    print("    ✅HISTÓRICO NA PISTA CALCULADO")
    return df_sorted

#if __name__ == "__main__":
#    print("--- Iniciando Teste de Engenharia de Features ---")
#    
#    sample_data = {
#        'season': [2023, 2023, 2023, 2023, 2023, 2023, 2024, 2024, 2024, 2024],
#        'round': [1, 1, 2, 2, 3, 3, 1, 1, 2, 2],
#        'circuit_location': ['Sakhir', 'Sakhir', 'Jeddah', 'Jeddah', 'Sakhir', 'Sakhir', 'Sakhir', 'Sakhir', 'Jeddah', 'Jeddah'],
#        'date': ['2023-03-05', '2023-03-05', '2023-03-19', '2023-03-19', '2023-04-02', '2023-04-02', '2024-03-04', '2024-03-04', '2024-03-18', '2024-03-18'],
#        'driverId': ['max_verstappen', 'perez', 'max_verstappen', 'perez', 'max_verstappen', 'perez', 'max_verstappen', 'perez', 'max_verstappen', 'perez'],
#        'constructorId': ['red_bull', 'red_bull', 'red_bull', 'red_bull', 'red_bull', 'red_bull', 'red_bull', 'red_bull', 'red_bull', 'red_bull'],
#        'grid': [1, 2, 1, 15, 1, 3, 1, 2, 2, 1],
#        'position': [1, 2, 2, 1, 3, 18, 1, 2, 1, 3],
#        'status': ['Finished', 'Finished', 'Finished', 'Finished', 'Finished', 'Collision', 'Finished', 'Finished', 'Finished', 'Finished'],
#        'points': [25.0, 18.0, 18.0, 25.0, 15.0, 0.0, 25.0, 18.0, 25.0, 15.0]
#    }
#    test_df = pd.DataFrame(sample_data)
#
#    preprocessed_df = preprocess_data(test_df)
#    
#    rolling_df = calculate_rolling_features(preprocessed_df, window=3)
#
#    features_df = calculate_track_features(rolling_df)
#    
#    print("\n--- DataFrame Final com Features (Amostra) ---")
#    cols_to_show = [
#        'season', 'round', 'circuit_location', 'driverId', 'position', 'is_dnf',
#        'driver_recent_points', 'constructor_recent_points', 
#        'driver_track_avg_pos', 'driver_track_dnf_rate' 
#    ]
#    print(features_df[cols_to_show])
#        
#    print("\n--- Teste de Engenharia de Features Concluído ---")