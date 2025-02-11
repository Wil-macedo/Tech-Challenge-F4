# Auto run da aplicação FLASK no EC2.


[Unit]
Description=Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Tech-Challenge-F4
ExecStart=/bin/bash -c 'source /home/ubuntu/Tech-Challenge-F4/venv/bin/activate && python3 /home/ubuntu/Tech-Challenge-F4/app.py'
Restart=always
Environment=PATH=/usr/bin:/usr/local/bin
Environment=FLASK_APP=/home/ubuntu/Tech-Challenge-F4/app.py

[Install]
WantedBy=multi-user.target


# LOGO APÓS:

sudo systemctl daemon-reload           # Recarregar as configurações do systemd
sudo systemctl restart flask_app       # Reiniciar o serviço

# VERIFICAR O STATUS.
sudo systemctl status flask_app

# RESET SERVICE:
sudo systemctl restart flask_app    # Reinicie o serviço que você criou anteriormente

