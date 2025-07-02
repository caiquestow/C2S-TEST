from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Veiculo(Base):
    __tablename__ = 'veiculos'

    id = Column(Integer, primary_key=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    motorizacao = Column(String, nullable=False)
    tipo_combustivel = Column(String, nullable=False)
    cor = Column(String, nullable=False)
    quilometragem = Column(Integer, nullable=False)
    numero_portas = Column(Integer, nullable=False)
    transmissao = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    placa = Column(String, unique=True, nullable=False)
    categoria = Column(String, nullable=False) 