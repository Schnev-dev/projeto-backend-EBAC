#API de livros
#endpoint
#POST - Adicionar novo livro
#GET -Buscar os dados dos livros
#PUT - Atualizar os dados de um livro
#DELETE - Remover um livro

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os

app = FastAPI(
title="API de Livros",
description="API para gerenciar livros",version="1.0.0" ,
contact={
    "name": "Schnev Thompson",
    "email": "schnevthompson@proton.me"
}
)

MEU_USARIO = "admin"
MINHA_SENHA = "admin"

security = HTTPBasic()

meus_livrozinhos = {}
class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

def authenticar_meu_usarion(credentials: HTTPBasicCredentials = Depends(security)):
    is_correct_username = secrets.compare_digest(credentials.username, MEU_USARIO)
    is_correct_password = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=401,
            detail="Usario ou senha incorretos.",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/livros")
def get_livros(page: int = 1, limit: int = 10, credentials: HTTPBasicCredentials = Depends(authenticar_meu_usarion)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Página e limite devem ser maiores que zero.")

    if not meus_livrozinhos:
        return {"message": "Nao existe nenhum livro!"}
    
    start = (page - 1) * limit
    end = start + limit

    livros_pagina = [
    {
        "id": id_livro,
        "nome_livro": livro_data["nome_livro"],
        "autor_livro": livro_data["autor_livro"],
        "ano_livro": livro_data["ano_livro"],
    }
    for id_livro, livro_data in list(meus_livrozinhos.items())[start:end]
]

    return {
    "page": page,
    "livros": livros_pagina,
    "limit": limit,
    "total_livros": len(meus_livrozinhos),
}

@app.post("/adicionar_livro")
def post_livro(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(authenticar_meu_usarion)):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400, detail="Esse Livro já existe meu parceiro!")
    meus_livrozinhos[id_livro] = livro.dict()
    return {"message": "Livro adicionado com sucesso!"}

@app.put("/atualizar/{id_livro}")
def put_livro(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(authenticar_meu_usarion)):
    meu_livro = meus_livrozinhos.get(id_livro)
    if  not  meu_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    meus_livrozinhos[id_livro] = livro.dict()
    return {"message": "As informações do seu Livro foram atualizadas com sucesso!"}

@app.delete("/remover/{id_livro}")
def delete_livro(id_livro: int, credentials: HTTPBasicCredentials = Depends(authenticar_meu_usarion)):
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=400, detail="Livro não foi encontrado.")
    del meus_livrozinhos[id_livro]
    return {"message": "Livro removido com sucesso!"}
