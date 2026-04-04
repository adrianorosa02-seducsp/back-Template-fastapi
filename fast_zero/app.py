from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Olá Mundo - Inetz Lab 05', 'aluno': 'arosa'}
