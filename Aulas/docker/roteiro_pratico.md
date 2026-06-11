O roteiro de atividade prática visa estruturar um ambiente composto por uma aplicação back-end (Node.js) e um banco de dados (MongoDB). Para atender aos requisitos de orquestração e isolamento descritos no plano de aula, a abordagem mais eficiente é o uso do Docker Compose, que permite definir e executar ambos os serviços de forma integrada e replicável.  Abaixo, apresento os comandos e a estrutura de configuração sugeridos para a atividade:1. Estrutura de ArquivosCrie um diretório para o projeto com a seguinte estrutura:docker-compose.yml: Arquivo de orquestração.Dockerfile (no diretório do back-end): Para definir a imagem da sua aplicação Node.js.2. Configuração do Orquestrador (docker-compose.yml)Este arquivo garante que o banco de dados seja inicializado antes da aplicação e estabelece uma rede interna segura.  
YAML ```
version: '3.8'
services:
  mongodb:
    image: mongo:latest
    container_name: db_mongo
    networks:
      - backend-network
    volumes:
      - mongo-data:/data/db

  backend:
    build: .
    container_name: app_node
    ports:
      - "3000:3000"
    depends_on:
      - mongodb
    environment:
      - MONGO_URL=mongodb://mongodb:27017/meubanco
    networks:
      - backend-network

networks:
  backend-network:
    driver: bridge

volumes:
  mongo-data:

```  
3. Comandos de Criação e GestãoUtilize os comandos abaixo para realizar as etapas práticas solicitadas no roteiro:  Subir o ambiente:Bashdocker-compose up -d
Este comando inicializa os serviços em segundo plano, respeitando a ordem de dependência definida.Verificar o status dos containers:Bashdocker-compose ps
Visualizar logs (para auditoria conforme solicitado):Bashdocker-compose logs -f
Parar e remover os containers:Bashdocker-compose down
Orientações para os Alunos (Baseado no Roteiro)Para concluir os objetivos pedagógicos, os estudantes devem atentar aos seguintes pontos durante a execução:  Isolamento: Observe que a aplicação não expõe a porta do MongoDB externamente, apenas a porta 3000 do Node.js, garantindo a segurança recomendada no item 3.1 do roteiro.  Rede Interna: O uso da backend-network permite que o container app_node se comunique com o db_mongo pelo nome do serviço, sem necessidade de IPs fixos.  Consistência: O uso de volumes garante que os dados do banco persistam mesmo se o container for removido.  