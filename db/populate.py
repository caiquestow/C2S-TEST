from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Veiculo
from faker import Faker
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'veiculos.db')
engine = create_engine(f'sqlite:///{DB_PATH}')
Session = sessionmaker(bind=engine)
session = Session()

# Cria as tabelas
Base.metadata.create_all(engine)

fake = Faker('pt_BR')

marcas_modelos = [
    ("Fiat", ["Uno", "Palio", "Argo", "Toro"]),
    ("Volkswagen", ["Gol", "Polo", "Virtus", "T-Cross"]),
    ("Chevrolet", ["Onix", "Prisma", "Tracker", "S10"]),
    ("Ford", ["Ka", "Fiesta", "EcoSport", "Ranger"]),
    ("Toyota", ["Corolla", "Etios", "Hilux", "Yaris"]),
    ("Honda", ["Civic", "Fit", "HR-V", "City"]),
    ("Hyundai", ["HB20", "Creta", "Tucson", "Azera"]),
    ("Renault", ["Sandero", "Logan", "Duster", "Kwid"]),
]

motorizacoes = ["1.0", "1.3", "1.6", "2.0", "2.2 Turbo", "3.0 V6"]
tipos_combustivel = ["Gasolina", "Etanol", "Flex", "Diesel", "GNV"]
cores = ["Preto", "Branco", "Prata", "Vermelho", "Azul", "Cinza"]
transmissoes = ["Manual", "Automático"]
categorias = ["Hatch", "Sedan", "SUV", "Picape"]

placas_usadas = set()

def gerar_placa():
    while True:
        placa = fake.unique.license_plate()
        if placa not in placas_usadas:
            placas_usadas.add(placa)
            return placa

for _ in range(100):
    marca, modelos = random.choice(marcas_modelos)
    modelo = random.choice(modelos)
    veiculo = Veiculo(
        marca=marca,
        modelo=modelo,
        ano=random.randint(2005, 2024),
        motorizacao=random.choice(motorizacoes),
        tipo_combustivel=random.choice(tipos_combustivel),
        cor=random.choice(cores),
        quilometragem=random.randint(0, 200000),
        numero_portas=random.choice([2, 4]),
        transmissao=random.choice(transmissoes),
        preco=round(random.uniform(20000, 200000), 2),
        placa=gerar_placa(),
        categoria=random.choice(categorias)
    )
    session.add(veiculo)

session.commit()
print(f'Banco populado com 100 veículos fictícios em {DB_PATH}.') 