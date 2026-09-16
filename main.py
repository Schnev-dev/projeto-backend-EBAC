#API de livros
#endpoint
#POST - Adicionar novo livro
#GET -Buscar os dados dos livros
#PUT - Atualizar os dados de um livro
#DELETE - Remover um livro

from fastapi import FastAPI, HTTPException

app = FastAPI()

meus_livrozinhos = {}

@app.get("/livros")
def get_livros():
    if not meus_livrozinhos:
        return {"message": "Nenhum livro encontrado."}
    else:
        return {"livros": meus_livrozinhos}

@app.post("/adicionar_livro")
def post_livro(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400, detail="Esse Livro já existe meu parceiro!")
    else:
        meus_livrozinhos[id_livro] = {"nome": nome_livro, "autor": autor_livro, "ano": ano_livro}
        return {"message": "Livro adicionado com sucesso!"}

@app.put("/atualizar/{id_livro}")
def put_livro(id_livro: int, nome_livro: str | None = None, autor_livro: str | None = None, ano_livro: int | None = None):
    meu_livro = meus_livrozinhos.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    else:
        if nome_livro:
            meu_livro[nome_livro] = nome_livro
        if autor_livro:
            meu_livro[autor_livro] = autor_livro
        if ano_livro:
            meu_livro[ano_livro] = ano_livro
            return {"message": "As informações do seu Livro foram atualizadas com sucesso!"}    

@app.delete("/remover{id_livro}")
def delete_livro(id_livro: int):
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=404, detail="Livro não foi encontrado.")
    else:
        del meus_livrozinhos[id_livro]
        return {"message": "Livro removido com sucesso!"}
