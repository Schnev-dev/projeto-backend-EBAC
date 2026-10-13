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

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./livros.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



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

class LivroDB(Base):
    __tablename__ = "Livros"

    id = Column(Integer, primary_key=True, index=True)
    nome_livro = Column(String, index=True)
    author_livro = Column(String, index=True)
    ano_livro = Column(Integer)
class Livro(BaseModel):
    nome_livro: str
    author_livro: str
    ano_livro: int

Base.metadata.create_all(bind=engine)

def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
def get_livros(page: int = 1, size: int = 10, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(authenticar_meu_usarion)):
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="Página e limit devem ser maiores que zero.")

    livros = db.query(LivroDB).offset((page-1)*size).limit(size).all()
    if not livros:
        return {"message": "Nao existe nenhum livro!"}

    total_livros = db.query(LivroDB).count()

    return {
    "page": page,
    "livros": [{"id": livro.id, "nome": livro.nome_livro, "author": livro.author_livro, "ano": livro.ano_livro } for livro in livros],
    "size": size,
    "total_livros": total_livros
}

@app.post("/adicionar_livro")
def post_livro(livro: Livro, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(authenticar_meu_usarion)):
    db_livro = db.query(LivroDB).filter(LivroDB.nome_livro == livro.nome_livro, LivroDB.author_livro == livro.author_livro).first()
    if db_livro:
        raise HTTPException(status_code=400, detail="Esse Livro já existe meu parceiro!")
    novo_livro = LivroDB(nome_livro=livro.nome_livro, author_livro=livro.author_livro, ano_livro=livro.ano_livro)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return {"message": "Livro adicionado com sucesso!"}

@app.put("/atualizar/{id_livro}")
def put_livro(id_livro: int, livro: Livro,db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(authenticar_meu_usarion)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado.")
    db_livro.nome_livro = livro.nome_livro
    db_livro.author_livro = livro.author_livro
    db_livro.ano_livro = livro.ano_livro
    db.commit() 
    db.refresh(db_livro)
    return {"message": "Livro atualizado com sucesso!"}

@app.delete("/remover/{id_livro}")
def delete_livro(id_livro: int, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(authenticar_meu_usarion)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado.")
    db.delete(db_livro)
    db.commit()
    return {"message": "Livro removido com sucesso!"}
