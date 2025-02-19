1️⃣ Construir a imagem do Docker:

docker login
docker build -t tech_challenge_f4 .

docker tag tech_challenge_f4 willmacedo1/tc_fase_4
docker push willmacedo1/tc_fase_4

# Baixar container:
    * docker pull willmacedo1/tc_fase_4

# SUBIR CONTAINER NO DOCKER HUB:

docker tag nome_da_imagem seu_usuario_dockerhub/nome_do_repositorio:tag
docker push seu_usuario_dockerhub/nome_do_repositorio:tag

### RODANDO CONTAINER:

docker run -p 8010:8010 tech_challenge_f4
# NO EC2
sudo docker run -d --restart=always -p 8010:8010 --name tc_fase_4 willmacedo1/tc_fase_4

URL da aplicação:
    * https://ec2-18-234-186-76.compute-1.amazonaws.com:8010/
