# 📘 Aula-01: Verbos, Status Codes e Contratos (Pydantic)

Bem-vindo à primeira aula prática de desenvolvimento de APIs com **FastAPI** e **Python 3.13**. Hoje vamos entender como os sistemas conversam "sob o capô".

---

## 1. O Protocolo HTTP: Verbos e Intenções
Quando um cliente faz uma requisição, ele indica sua intenção ao servidor através de **Verbos**:

* **GET**: Utilizado para **recuperar** recursos. Solicita um dado já existente.
* **POST**: Permite **criar** um novo recurso (ex: registrar um usuário).
* **PUT**: **Atualiza** um recurso existente por completo.
* **DELETE**: **Exclui** um recurso específico do sistema.

No FastAPI, definimos isso diretamente no decorador da função:

@app.get('/')
def read_root():
    return {'message': 'Olá Mundo - Inetz Lab 05', 'aluno': 'arosa'}

---

## 2. Códigos de Resposta (Status Codes)
O servidor sempre responde com um código que indica o resultado da operação:

| Faixa | Significado | Exemplo Comum |
| :--- | :--- | :--- |
| **1xx** | Informativo | Recebido e processando. |
| **2xx** | **Sucesso** | 200 OK, 201 Created. |
| **3xx** | Redirecionamento | 301 Moved Permanently. |
| **4xx** | **Erro no Cliente** | 404 Not Found, 422 Unprocessable Entity. |
| **5xx** | **Erro no Servidor** | 500 Internal Server Error. |

### Explicitando o Status no FastAPI:
Para profissionalizar a API, usamos a biblioteca nativa do Python para definir o status de sucesso:
```python
from http import HTTPStatus

@app.get("/", status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}

```

## 3. APIs vs HTML
Diferente de sites convencionais que retornam **HTML** (focado em visual/apresentação), nossas APIs focam na **transferência de dados**.

* **Mídia Padrão:** O **JSON** (JavaScript Object Notation). 
* **Vantagem:** O mesmo JSON pode ser lido por qualquer sistema (Android, iOS, Web ou outros servidores).

---

## 4. Contratos de Dados com Pydantic
Para garantir que o JSON enviado ou recebido esteja correto, utilizamos **Schemas** (Contratos). No FastAPI, o **Pydantic** faz esse trabalho.

### Passo Prático 01: Criando fast_zero/schemas.py
Crie este arquivo para definir a estrutura da sua mensagem (o contrato):
```python
from pydantic import BaseModel

class Message(BaseModel):
    message: str
```

### Passo Prático 02: Aplicando no fast_zero/app.py
Agora, amarramos o contrato à rota para garantir a validação:
```python
from http import HTTPStatus
from fastapi import FastAPI
from fast_zero.schemas import Message # Importando o Schema

app = FastAPI()

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}

```

## 📖 5. Onde ver o resultado?
Após salvar, acesse os subdomínios do seu laboratório:

1. **Swagger UI**: [https://lab05.inetz.com.br/docs](https://lab05.inetz.com.br/docs)
2. **ReDoc**: [https://lab05.inetz.com.br/redoc](https://lab05.inetz.com.br/redoc)

Observe que o seu modelo **Message** agora aparece documentado na seção de **Schemas** no final da página.

---

### 🚩 Desafio da Aula
Altere o valor da chave message no seu app.py para seu nome e verifique se a documentação e a resposta da API refletem a mudança.
Explique no seu caderno o que aconteceu e porque.