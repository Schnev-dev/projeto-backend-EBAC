#API de livros
#endpoint
#POST - Adicionar novo livro
#GET -Buscar os dados dos livros
#PUT - Atualizar os dados de um livro
#DELETE - Remover um livro

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import optional

app = FastAPI()

meus_livrozinhos = {}
class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int



@app.get("/livros")
def get_livros():
    if not meus_livrozinhos:
        return {"message": "Nenhum livro encontrado."}
    return {"livros": meus_livrozinhos}

@app.post("/adicionar_livro")
def post_livro(id_livro: int, livro: Livro):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400, detail="Esse Livro já existe meu parceiro!")
    meus_livrozinhos[id_livro] = livro.dict()
    return {"message": "Livro adicionado com sucesso!"}

@app.put("/atualizar/{id_livro}")
def put_livro(id_livro: int, livro: Livro):
    meu_livro = meus_livrozinhos.get(id_livro)
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    meu_livro[id_livro] = livro.dict()
    return {"message": "As informações do seu Livro foram atualizadas com sucesso!"}

@app.delete("/remover/{id_livro}")
def delete_livro(id_livro: int):
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=404, detail="Livro não foi encontrado.")
    del meus_livrozinhos[id_livro]
    return {"message": "Livro removido com sucesso!"}
