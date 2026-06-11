# APOIO DA ATIVIDADE

O roteiro de atividade prática visa estruturar um ambiente composto por uma aplicação back-end (Node.js) e um banco de dados (MongoDB). Para atender aos requisitos de orquestração e isolamento descritos no plano de aula, a abordagem mais eficiente é o uso do Docker Compose, que permite definir e executar ambos os serviços de forma integrada e replicável.

Abaixo, apresento os comandos e a estrutura de configuração sugeridos para a atividade:
  1. Estrutura de Arquivos: Crie um diretório para o projeto com a seguinte estrutura:
  
  docker-compose.yml: Arquivo de orquestração.
  Dockerfile (no diretório do back-end): Para definir a imagem da sua aplicação Node.js.

  2. Configuração do Orquestrador (docker-compose.yml)
  Este arquivo garante que o banco de dados seja inicializado antes da aplicação e estabelece uma rede interna segura. Deve estar no nosso projeto fastapi na raiz fast_zero.  

 
```
version: '3.8'
services:
  backend:
    build: .
    container_name: app_fastapi
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - MONGO_URL=mongodb://mongodb:27017/meubanco
    depends_on:
      - mongodb

  mongodb:
    image: mongo:latest
    container_name: db_mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```  
DockerFile (Já existente deve estar assim)

```
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "fast_zero.app:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
```
3. Comandos de Criação e Gestão: Utilize os comandos abaixo para realizar as etapas práticas solicitadas no roteiro:  

**Subir o ambiente:**
```
Bash docker-compose up -d
```
Este comando inicializa os serviços em segundo plano, respeitando a ordem de dependência definida.

**Verificar o status dos containers:** 
```
Bash docker-compose ps
```
**Visualizar logs (para auditoria conforme solicitado):**
```
Bash docker-compose logs -f
```

**Parar e remover os containers:**
```
Bash docker-compose down
```
Orientações para os Alunos (Baseado no Roteiro)Para concluir os objetivos pedagógicos, os estudantes devem atentar aos seguintes pontos durante a execução:  Isolamento: Observe que a aplicação não expõe a porta do MongoDB externamente, apenas a porta 3000 do Node.js, garantindo a segurança recomendada no item 3.1 do roteiro.  Rede Interna: O uso da backend-network permite que o container app_node se comunique com o db_mongo pelo nome do serviço, sem necessidade de IPs fixos.  Consistência: O uso de volumes garante que os dados do banco persistam mesmo se o container for removido.  