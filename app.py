from flask import Flask, request, jsonify
from modelPredict import *
import pandas as pd
import psutil 
import time

app = Flask(__name__)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
    Recebe um array com os últimos 60 preços de fechamento e retorna a previsão do próximo dia.
    Também monitora o tempo de resposta e uso de recursos do sistema.
    """
    start_time = time.time()  # Iniciar medição de tempo
    
    data:dict = request.json  # Obtém os dados do corpo da requisição

    for key, value in data.items():
        if len(value) != 60:
            return {key: "Forneça exatamente 60 preços de fechamento para previsão."}

        prediction = modelPredict(value)
        
        # Medir tempo de resposta e uso de recursos
        response_time = round(time.time() - start_time, 4)  # Tempo em segundos
        cpu_usage = psutil.cpu_percent()  # Porcentagem de uso da CPU
        memory_usage = psutil.virtual_memory().percent  # Uso de memória em %

        # Log de previsões
        log_data = {
            "timestamp": pd.Timestamp.now(),
            "real_price": value[-1],  # Último preço real fornecido
            "predicted_price": round(prediction, 2),
            "response_time": response_time,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
        }

        # Salvar logs em CSV
        log_df = pd.DataFrame([log_data])
        log_df.to_csv("log_predictions.csv", mode="a", header=not pd.io.common.file_exists("log_predictions.csv"), index=False)

        result = jsonify({
            "predicted_price": prediction,
            "response_time_sec": response_time,
            "cpu_usage_percent": cpu_usage,
            "memory_usage_percent": memory_usage,
        })

        return result

# --- 6. MONITORAMENTO ---
@app.route("/monitor/")
def monitor():
    """
    Retorna o status do sistema, incluindo uso de CPU, memória e tempo médio de resposta baseado nos logs.
    """
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    try:
        log_df = pd.read_csv("log_predictions.csv")
        avg_response_time = round(log_df["response_time"].mean(), 4)
    except FileNotFoundError:
        avg_response_time = "Nenhum dado disponível"

    return {
        "cpu_usage_percent": cpu_usage,
        "memory_usage_percent": memory_usage,
        "avg_response_time_sec": avg_response_time
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8010")