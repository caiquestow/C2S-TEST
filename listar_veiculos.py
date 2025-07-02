# script para listar veiculos no banco de dados
#    python3 listar_veiculos.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Veiculo

engine = create_engine('sqlite:///db/veiculos.db')
Session = sessionmaker(bind=engine)
session = Session()

for v in session.query(Veiculo).all():
    print(f"{v.marca} {v.modelo} | Ano: {v.ano} | Cor: {v.cor} | Combustível: {v.tipo_combustivel} | Preço: R$ {v.preco:.2f}")

session.close() 