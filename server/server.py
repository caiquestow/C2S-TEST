from fastapi import FastAPI, Query
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from db.models import Veiculo, Base
from typing import List, Optional
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../db/veiculos.db')
engine = create_engine(f'sqlite:///{os.path.abspath(DB_PATH)}')
Session = sessionmaker(bind=engine)

# Endpoint para recuperar veículos com filtros dinâmicos.
@app.get("/veiculos", response_model=List[dict])
def buscar_veiculos(
    marca: Optional[List[str]] = Query(None),
    modelo: Optional[List[str]] = Query(None),
    ano: Optional[int] = Query(None),
    tipo_combustivel: Optional[List[str]] = Query(None),
    cor: Optional[List[str]] = Query(None),
    transmissao: Optional[List[str]] = Query(None),
    categoria: Optional[List[str]] = Query(None),
    preco: Optional[int] = Query(None),
):
    session = Session()
    filtros = []
    if marca:
        filtros.append(or_(*[Veiculo.marca.ilike(f"%{m}%") for m in marca]))
    if modelo:
        filtros.append(or_(*[Veiculo.modelo.ilike(f"%{m}%") for m in modelo]))
    if ano:
        filtros.append(Veiculo.ano >= ano)
    if tipo_combustivel:
        filtros.append(or_(*[Veiculo.tipo_combustivel.ilike(f"%{c}%") for c in tipo_combustivel]))
    if cor:
        filtros.append(or_(*[Veiculo.cor.ilike(f"%{c}%") for c in cor]))
    if transmissao:
        filtros.append(or_(*[Veiculo.transmissao.ilike(f"%{t}%") for t in transmissao]))
    if categoria:
        filtros.append(or_(*[Veiculo.categoria.ilike(f"%{cat}%") for cat in categoria]))
    if preco:
        filtros.append(Veiculo.preco <= preco)
    query = session.query(Veiculo)
    if filtros:
        query = query.filter(and_(*filtros))
    resultados = query.all()
    session.close()
    return [
        {
            "marca": v.marca,
            "modelo": v.modelo,
            "ano": v.ano,
            "motorizacao": v.motorizacao,
            "tipo_combustivel": v.tipo_combustivel,
            "cor": v.cor,
            "quilometragem": v.quilometragem,
            "numero_portas": v.numero_portas,
            "transmissao": v.transmissao,
            "preco": v.preco,
            "placa": v.placa,
            "categoria": v.categoria
        }
        for v in resultados
    ] 