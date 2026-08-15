from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="ShoopTree - Serviço de Produtos")

def get_db():
    conn = sqlite3.connect("produtos.db")
    conn.row_factory = sqlite3.Row
    return conn

# Inicializa o banco de dados isolado do microsserviço
with get_db() as db:
    db.execute('''CREATE TABLE IF NOT EXISTS produtos 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, preco REAL)''')

class Produto(BaseModel):
    nome: str
    preco: float

@app.post("/produtos", status_code=201)
def criar_produto(produto: Produto):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (produto.nome, produto.preco))
        db.commit()
        return {"id": cursor.lastrowid, "nome": produto.nome, "preco": produto.preco}

@app.get("/produtos")
def listar_produtos():
    with get_db() as db:
        produtos = db.execute("SELECT * FROM produtos").fetchall()
        return [dict(p) for p in produtos]

# Para rodar no terminal do PyCharm: uvicorn produtos_service:app --port 8001 --reload