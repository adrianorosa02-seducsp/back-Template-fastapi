📘 Aula-01: Fundamentos de APIs e Contratos com FastAPI
Nesta aula, vamos mergulhar no funcionamento da web moderna e entender como os sistemas conversam entre si.

⚡ 1. O Protocolo HTTP: Verbos e Intenções
Quando um cliente (navegador, celular, outro servidor) faz uma requisição, ele utiliza verbos para indicar o que deseja:

GET: Recuperar dados existentes.

POST: Criar um novo recurso (ex: cadastrar usuário).

PUT: Atualizar um recurso existente.

DELETE: Remover um recurso específico.

No FastAPI, mapeamos esses verbos usando decoradores:

Python

@app.get('/')
def read_root():
    return {'message': 'Olá Mundo - Inetz Lab 05', 'aluno': 'arosa'}
🚦 2. Códigos de Resposta (Status Codes)
O servidor responde com códigos numéricos para dizer o que aconteceu:

1xx (Informativo): Requisição recebida.

2xx (Sucesso): Tudo certo! (Ex: 200 OK, 201 Created).

3xx (Redirecionamento): Vá para outro lugar.

4xx (Erro no Cliente): Você fez algo errado (Ex: 404 Not Found, 422 Unprocessable Entity).

5xx (Erro no Servidor): Eu (servidor) quebrei (Ex: 500 Internal Server Error).

Dica Inetz: Use a biblioteca nativa do Python para maior clareza:

Python

from http import HTTPStatus
@app.get("/", status_code=HTTPStatus.OK)
📦 3. Além do HTML: O Reinado do JSON
Enquanto o HTML foca em apresentação (visual), as APIs focam em transferência de dados. O padrão ouro aqui é o JSON (JavaScript Object Notation).

Exemplo de JSON:

JSON

{
    "livros": [
        {
            "titulo": "O apanhador no campo de centeio",
            "autor": "J.D. Salinger",
            "ano": 1945,
            "disponivel": false
        }
    ]
}
📜 4. Contratos e Schemas com Pydantic
Para que o cliente e o servidor se entendam sem erros, usamos Schemas (Contratos). No Python, a ferramenta líder é o Pydantic.

Ele garante a validação e gera a documentação automática.

Criando seu primeiro Schema (schemas.py):
Python

from pydantic import BaseModel

class Message(BaseModel):
    message: str
Integrando com o FastAPI:
Python

from http import HTTPStatus
from fastapi import FastAPI
from .schemas import Message # Importando seu contrato

app = FastAPI()

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
📖 5. Documentação Automática
Uma das maiores vantagens dessa abordagem é que sua API se documenta sozinha:

Swagger UI: https://lab05.inetz.com.br/docs (Interativo para testes).

ReDoc: https://lab05.inetz.com.br/redoc (Documentação técnica limpa).

📝 Resumo do Analista
Nesta Aula-01, transformamos um simples "Olá Mundo" em uma aplicação profissional que respeita códigos HTTP, utiliza contratos de dados (Pydantic) e oferece documentação automática.