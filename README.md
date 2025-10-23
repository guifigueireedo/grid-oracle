# 🏎️🤖 F1 Pódium Predictor & MLOps

Este projeto é um sistema completo de Machine Learning para prever os resultados de corridas de Fórmula 1, desde a coleta de dados até a implantação de um ciclo de retreinamento automático (MLOps).

**[Clique aqui para ver o app ao vivo!](URL_DO_SEU_APP_STREAMLIT_AQUI)** (Você adicionará isso quando fizer o deploy)

## 🎯 O Que o Projeto Faz?

O sistema prevê a posição final de todos os 20 pilotos para a próxima corrida de F1 e gera uma explicação em linguagem natural para as previsões do Top 5, usando IA Generativa.

O mais importante é que este projeto é um **ciclo de MLOps vivo**:

1.  **Sábado (Pré-Corrida):** Automaticamente coleta a posição de largada, previsão do tempo e inputs manuais sobre atualizações de carro.
2.  **Sábado (Previsão):** Roda o modelo de ML treinado e publica as previsões no app Streamlit.
3.  **Segunda (Pós-Corrida):** Automaticamente baixa os resultados reais da corrida, compara com as previsões (calculando a precisão) e **retreina o modelo** com esses novos dados, deixando-o mais inteligente para a próxima semana.

## ✨ Features Principais

* **Previsão de Posição:** Um modelo `XGBRegressor` que prevê a posição final de cada piloto.
* **Previsão de DNF:** Um modelo `LogisticRegression` que prevê a probabilidade de cada piloto não terminar a corrida.
* **Explicações com IA:** Usa a **API Gemini** do Google para traduzir os *outputs* técnicos do modelo (SHAP) em explicações fáceis de entender.
* **Engenharia de Features Complexa:** O modelo não usa apenas a posição de largada, mas também:
    * Forma recente do piloto (média de pontos nas últimas 3 corridas).
    * Histórico do piloto *naquele circuito específico* (média de posição, taxa de DNF).
    * Previsão do tempo (chuva, seco).
    * Input manual de "atualizações de carro".
* **MLOps 100% Automatizado:** Usa **GitHub Actions** para agendar os scripts de coleta, previsão e retreinamento.
* **Hospedagem Gratuita:**
    * **Código:** GitHub
    * **App (Frontend):** Streamlit Community Cloud
    * **Modelos & Datasets:** Hugging Face Hub

## 🛠️ Tech Stack

* **Python**
* **ML/Data:** Pandas, Scikit-learn, XGBoost, SHAP
* **Frontend:** Streamlit
* **APIs:** Ergast (Dados F1), OpenWeatherMap (Clima), Google Gemini (IA Generativa)
* **MLOps:** GitHub Actions, Hugging Face Hub (para versionamento de modelos e datasets)

## 🚀 Como Rodar Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/f1-predictor.git](https://github.com/SEU-USUARIO/f1-predictor.git)
    cd f1-predictor
    ```

2.  **Crie um ambiente virtual e instale as dependências:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # (ou .venv\Scripts\activate no Windows)
    pip install -r requirements.txt
    ```

3.  **Configure suas chaves de API:**
    * Copie o `.env.example` para um novo arquivo chamado `.env`.
    * Preencha o `.env` com suas chaves reais do Google AI Studio, OpenWeatherMap e Hugging Face.

4.  **Rode o aplicativo Streamlit:**
    ```bash
    streamlit run app.py
    ```