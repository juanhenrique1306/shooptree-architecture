from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="ShoopTree - Serviço de Pagamentos")

def get_db():
    conn = sqlite3.connect("pagamentos.db")
    conn.row_factory = sqlite3.Row
    return conn

with get_db() as db:
    db.execute('''CREATE TABLE IF NOT EXISTS pagamentos 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, pedido_id INTEGER, valor REAL, status TEXT)''')

class Pagamento(BaseModel):
    pedido_id: int
    valor: float

@app.post("/pagamentos", status_code=201)
def processar_pagamento(pagamento: Pagamento):
    with get_db() as db:
        cursor = db.cursor()
        # Em um cenário real, integraria com o gateway aqui
        cursor.execute("INSERT INTO pagamentos (pedido_id, valor, status) VALUES (?, ?, ?)",
                       (pagamento.pedido_id, pagamento.valor, "APROVADO"))
        db.commit()
        return {"mensagem": "Pagamento processado com sucesso", "status": "APROVADO"}

@app.get("/pagamentos")
def listar_pagamentos():
    with get_db() as db:
        pagamentos = db.execute("SELECT * FROM pagamentos").fetchall()
        return [dict(p) for p in pagamentos]

# Para rodar no terminal do PyCharm: uvicorn pagamentos_service:app --port 8002 --reload