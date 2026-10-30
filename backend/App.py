from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

app = FastAPI();

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserModel (BaseModel):
    nome: str
    senha: str