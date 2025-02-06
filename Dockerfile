# Usa uma imagem base do Python
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Define a variável de ambiente para evitar buffers de saída
ENV PYTHONUNBUFFERED=1

# Expõe a porta 5000 para acesso externo
EXPOSE 8010

# Comando para rodar a aplicação
CMD ["python", "app.py"]
