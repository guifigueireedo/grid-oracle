import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import sys
import os
import json
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from src import config
    from src import collect
    from src import features
except ImportError:
    import config
    import collect
    import features

#=== DEFINIÇÃO DE FEATURES ===
FEATURES_TO_USE = [
    'season',
    'round',
    #'circuit-location',
    'grid',
    'driver_recent_points',
    'constructor_recent_points',
    'driver_track_avg_pos',
    'driver_track_dnf_rate',
]

TARGET_POSITION = 'position'
TARGET_DNF = 'is_dnf'

#=== PROCESSO DE TREINAMENTO ===
def train_models(start_year: int, end_year: int):
    print("🚀INICIANDO PIPELINE DE TREINAMENTO")

    print(f"    💾 CARREGANDO DADOS DE {start_year} a {end_year}")
    raw_df = collect.fetch_race_results(start_year=start_year, end_year=end_year)

    if raw_df.empty:
        print("    ❌NENHUM DADO ENCONTRADO PRA ESSE PERÍODO")
        return
    
    print("    ⚙️APLICANDO ENGENHARIA DE FEATURES")
    preprocessed_df = features.preprocess_data(raw_df)
    rolling_df = features.calculate_rolling_features(preprocessed_df, window=5)
    final_df = features.calculate_track_features(rolling_df)

    print("    📊CODIFICANDO FEATURES CATEGÓRICAS")
    final_df = pd.get_dummies(final_df, columns=['circuit_location'], prefix='track')

    all_features = FEATURES_TO_USE.copy()

    track_columns = [col for col in final_df.columns if col.startswith('track_')]
    all_features.extend(track_columns)

    final_df[all_features] = final_df[all_features].fillna(0)

    print("    ✅ENGENHARIA DE FEATURES CONCLUÍDA")

    print("    🎯SEPARANDO FEATURES E ALVOS")
    X = final_df[all_features]
    y_pos = final_df[TARGET_POSITION]
    y_dnf = final_df[TARGET_DNF]

    print("    🎯TREINANDO MODELO DE POSIÇÃO")
    pos_model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )
    pos_model.fit(X, y_pos)
    print("    ✅MODELO DE POSIÇÃO TREINADO")

    print("    💥TREINANDO MODELO DE DNF")
    dnf_model = LogisticRegression(
        solver='liblinear',
        random_state=42,
        class_weight='balanced'
    )
    dnf_model.fit(X, y_dnf)
    print("    ✅MODELO DE DNF TREINADO")

    print("    💾SALVANDO MODELOS TREINADOS")

    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)

    pos_model_path = os.path.join(models_dir, config.POSITION_MODEL_FILENAME)
    dnf_model_path = os.path.join(models_dir, config.DNF_MODEL_FILENAME)
    metadata_path = os.path.join(models_dir, config.MODEL_METADATA_FILENAME)

    joblib.dump(pos_model, pos_model_path)
    joblib.dump(dnf_model, dnf_model_path)

    metadata = {
        'training_timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'training_data_start_year': start_year,
        'training_data_end_year': end_year,
        'features_used': all_features,
        'target_position': TARGET_POSITION,
        'target_dnf': TARGET_DNF,
        'xgboost_params': pos_model.get_params(),
        'logistic_regression_params': dnf_model.get_params()
    }
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)

    print(f"    ✅MODELOS SALVOS EM: {pos_model_path}, {dnf_model_path}")
    print(f"    ✅METADATAS SALVOS EM: {metadata_path}")

    print("🏁PIPELINE DE TREINAMENTO CONCLUÍDO")

if __name__ == "__main__":
    TRAIN_START_YEAR = 2018 
    TRAIN_END_YEAR = datetime.now().year - 1
    
    train_models(start_year=TRAIN_START_YEAR, end_year=TRAIN_END_YEAR)