1️⃣ Construir a imagem do Docker:

docker build -t tech_challenge_f4 .

### RODANDO CONTAINER:

docker run -p 8010:8000 tech_challenge_f4



###RODAND:

gunicorn -c gunicorn.conf.py app:app

gunicorn --workers 3 --bind 0.0.0.0:8010 app:app


# PARA RODAS O PROJETO NO WINDOWS UTILIZANDO WSL & Deploy EC2.

sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-venv python3-pip -y

python3 -m venv ~/venv
source ~/venv/bin/activate
sudo apt install gunicorn
pip install --no-cache-dir -r requirements.txt

