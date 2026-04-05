# 📘 Aula-01: Verbos, Status Codes e Contratos (Pydantic)

Bem-vindo à primeira aula prática de desenvolvimento de APIs com **FastAPI** e **Python 3.13**. Hoje vamos entender como a internet realmente funciona "sob o capô".

---

## 1. O Protocolo HTTP: Verbos e Intenções
Quando um cliente faz uma requisição, ele indica sua intenção ao servidor através de **Verbos**:

* **`GET`**: Utilizado para **recuperar** recursos. Solicita um dado já existente.
* **`POST`**: Permite **criar** um novo recurso (ex: registrar um usuário).
* **`PUT`**: **Atualiza** um recurso existente por completo.
* **`DELETE`**: **Exclui** um recurso específico do sistema.

No FastAPI, definimos isso diretamente no decorador da função:
```python
@app.get('/')
def read_root():
    return {'message': 'Olá Mundo - Inetz Lab 05', 'aluno': 'arosa'}