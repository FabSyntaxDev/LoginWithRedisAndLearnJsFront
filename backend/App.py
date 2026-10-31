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

class CadastrarUserModel (BaseModel):
    nome: str
    senha: str
    idade: int

@app.post("/login")
async def Login (user: UserModel):

    for i in range(20):
        if user.nome == r.hget((str(i)),'nome') and user.senha == r.hget((str(i)), 'senha'):
            return {"nome": "Bem-Vindo"}
    return {
        "nome": "Usuario não existe"
    }

@app.post("/adicionar_user")
async def AdicionarUser(user: CadastrarUserModel):
    # Geralmente maioridade é >= 18, ajuste se necessário
    if user.idade >= 18:
        for i in range(30):
            # Verifica se o campo 'nome' não existe (retorna None)
            if r.hget(str(i), 'nome') is None:
                r.hset(str(i), mapping={
                    "nome": user.nome,
                    "senha": user.senha,
                    "idade": user.idade 
                })
                # Retorna imediatamente assim que achar a vaga e cadastrar
                valor = str(i)
                dados = r.hgetall(valor)
                print(f"Dados: {dados} | id: {valor}")
                return {'nome': "Usuario Cadastrado"}
        
        # Caso o loop acabe e nenhum dos 30 slots esteja livre:
        return {'nome': "Limite de usuários atingido"}

    return {'nome': "Menor de idade não pode"}
            

@app.post("/adicionar_user_test")
async def Adicionar_user_test (user: UserModel):
    r.hset('1', mapping={
        'nome': user.nome,
        'senha': user.senha
    })

    print(r.hget('1', 'nome'))