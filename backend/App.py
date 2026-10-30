from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

app = FastAPI();

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserModel (BaseModel):
    nome: str = Field(min_length=2, max_length=24)
    senha: str = Field(min_length=6, max_length=32)

@app.post("/login")
async def Login (user: UserModel):

    for i in range(20):
        if user.nome == r.hget((str(i)),'nome') and user.senha == r.hget((str(i)), 'senha'):
            return {"nome": "Bem-Vindo"}
    return {
        "nome": "Usuario não existe"
    }



@app.post("/adicionar_user_test")
async def Adicionar_user_test (user: UserModel):
    r.hset('1', mapping={
        'nome': user.nome,
        'senha': user.senha
    })

    print(r.hget('1', 'nome'))