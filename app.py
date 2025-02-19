from flask import Flask, redirect, request, jsonify, render_template, make_response
from flask_compress import Compress
from flasgger import Swagger
from modelPredict import *
import pandas as pd
import subprocess
import threading
import psutil 
import time

app = Flask(__name__)
Compress(app)  # Habilita a compressão
laodModel()  # Garante que modelo está carregado, para rapida resposta.

try:
    app.config['SWAGGER'] = {
        'openapi': '3.0.1'
    }

    swagger = Swagger(app, template_file='swagger.yaml')

except Exception as ex:
    print("FALHA Swagger")
    
    
# Função para iniciar o MLflow UI
def run_mlflow_ui():
    try:
        subprocess.run(["mlflow", "ui", "--port", "8020"])
    except Exception as ex:
        predict(f"FALHA MLFLOW: {ex}")


# Redireciona para o MLflow UI
@app.route('/')
def index():
    return "API IMPLANTADA EM 06-02-2025"


# Redireciona para o MLflow UI
@app.route('/mlflow')
def mlflow_redirect():
    return redirect("http://localhost:8020")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
        Recebe um array com os últimos 60 preços de fechamento e retorna a previsão do próximo dia.
        Também monitora o tempo de resposta e uso de recursos do sistema.
    """
    
    if request.method == "POST":
        start_time = time.time() 
        data:dict = request.json  
        
        for key, value in data.items():
            if len(value) != 60:
                return make_response(jsonify({"error": "Forneça exatamente 60 preços de fechamento para previsão."}), 400)


            prediction = modelPredict(value)
            
            # Medir tempo de resposta e uso de recursos
            response_time = round(time.time() - start_time, 4)  # Tempo em segundos



            memory_usage = psutil.virtual_memory().percent  # Uso de memória em %
            result = jsonify({
                "predicted_price": prediction,
                "response_time_sec": response_time,
                "memory_usage_percent": memory_usage,
            })

            # Log de previsões
            log_data = {
                "timestamp": pd.Timestamp.now(),
                "response_time": response_time,
                "memory_usage": memory_usage,
            }
            # Salvar logs em CSV
            log_df = pd.DataFrame([log_data])
            log_df.to_csv("log_predictions.csv", mode="a", header=not pd.io.common.file_exists("log_predictions.csv"), index=False)

            return result

    else:
        return render_template("predictGet.html")


@app.route("/monitor")
def monitor():
    """
        Retorna o status do sistema, incluindo uso de CPU, memória e tempo médio de resposta baseado nos logs.
    """
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    try:
        log_df = pd.read_csv("log_predictions.csv")
        log_data = log_df.to_dict(orient="records")  # Retorna uma lista de dicionários, uma linha por dicionário

    except FileNotFoundError:
        log_data = "Nenhum dado disponível"

    return {
        "CURRENT CPU": cpu_usage,
        "MEMORY %": memory_usage,
        "RESPONSES": log_data
    }


if __name__ == "__main__":
    
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False

    # Inicia o MLflow UI em uma thread separada
    mlflow_thread = threading.Thread(target=run_mlflow_ui)
    mlflow_thread.start()

    app.run(host="0.0.0.0", port="8010")