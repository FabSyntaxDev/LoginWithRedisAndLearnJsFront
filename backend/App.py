from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import redis
import os
import shutil

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

os.makedirs("FotosPerfil", exist_ok=True)

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

class UserU (BaseModel):
    nome: str


class UserModel (BaseModel):
    nome: str = Field(min_length=2, max_length=24)
    senha: str = Field(min_length=6, max_length=32)

class CadastrarUserModel (BaseModel):
    nome: str = Field(min_length=2, max_length=24)
    senha: str = Field(min_length=2, max_length=24)
    idade: int

@app.post("/login")
async def Login (user: UserModel):

    for i in range(1000):
        if user.nome == r.hget((str(i)),'nome') and user.senha == r.hget((str(i)), 'senha'):
            return {"nome": "Bem-Vindo"}
    return {
        "nome": "Usuario não existe"
    }

@app.post("/adicionar_user")
async def AdicionarUser(user: CadastrarUserModel):
    if user.idade < 18:
        return {"erro": "Menor de idade não pode"}

    for i in range(1000):
        nome_atual = r.hget(str(i), "nome")
        if nome_atual == user.nome:
            return {"erro": "Usuário já existe"}

    for i in range(1000):
        if r.hget(str(i), "nome") is None:
            valor = str(i)
            r.hset(valor, mapping={
                "nome": user.nome,
                "senha": user.senha, 
                "idade": user.idade 
            })
                
            dados = r.hgetall(valor)
            print(f"Dados: {dados} | id: {valor}")
            return {"mensagem": "Usuário Cadastrado", "id": valor}

    return {"erro": "Limite de usuários atingido"}            


#agora vou adicionar as fotos
@app.post("/upload")
async def enviar_foto(user: str = Form(...), foto: UploadFile = File(...)):

    id_encontrado = None
    for i in range(1000):
        nome_atual = r.hget(str(i), "nome")
        if nome_atual == user:
            id_encontrado = str(i)
            break  # Achou, pode parar o loop

    if not id_encontrado:
        return {"erro": "Usuário não encontrado no Redis"}

    # Define o nome personalizado para a foto usando o ID encontrado
    prefixo = f"perfil_{id_encontrado}_"
    nome_personalizado = f"{prefixo}{foto.filename}"
        
    caminho_salvar = os.path.join("FotosPerfil", nome_personalizado)
        
    with open(caminho_salvar, "wb") as arquivo_local:
        shutil.copyfileobj(foto.file, arquivo_local)
            
    return {
        "mensagem": "Foto salva com sucesso!", 
        "usuario_id": id_encontrado,
        "foto_salva": nome_personalizado
    }






@app.post("/adicionar_user_test")
async def Adicionar_user_test (user: UserModel):
    r.hset('1', mapping={
        'nome': user.nome,
        'senha': user.senha
    })

    print(r.hget('1', 'nome'))