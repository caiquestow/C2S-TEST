import os
import requests
import openai
import json
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY", "")

SERVER_URL = "http://127.0.0.1:8000/veiculos"

# Schema para function calling
function_schema = {
    "name": "extrair_filtros_veiculo",
    "description": (
        "Extrai filtros de busca de veículos a partir de uma frase livre do usuário. "
        "Sempre normalize os valores para os exemplos fornecidos nas descrições dos campos. "
        "Retorne listas mesmo para um único valor."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "marca": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Marcas desejadas. Exemplo: ['Honda', 'Toyota']. Sempre retorne como lista, mesmo se houver apenas uma marca."
            },
            "modelo": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Modelos desejados. Exemplo: ['Civic', 'Corolla']. Sempre retorne como lista."
            },
            "ano": {
                "type": "integer",
                "description": "Ano mínimo do veículo. Exemplo: 2018. Se o usuário disser 'de 2015 pra frente', retorne 2015."
            },
            "tipo_combustivel": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Tipos de combustível. Exemplo: ['Flex', 'Gasolina', 'Diesel', 'Elétrico', 'Híbrido']. Normalize para essas opções."
            },
            "cor": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Cores desejadas. Exemplo: ['Preto', 'Branco', 'Prata', 'Vermelho', 'Azul']. Sempre retorne como lista."
            },
            "transmissao": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Tipo de transmissão. Exemplo: ['Automático', 'Manual', 'CVT']. Normalize para essas opções."
            },
            "categoria": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Categoria do veículo. Exemplo: ['Sedan', 'SUV', 'Hatch', 'Picape', 'Perua', 'Conversível', 'Minivan', 'Crossover']. Sempre normalize para uma dessas opções e retorne como lista."
            },
            "preco": {
                "type": "integer",
                "description": "Preço máximo em reais. Exemplo: 60000 para 'até 60 mil'."
            }
        },
        "required": []
    }
}

system_prompt = (
    "Você é um assistente que ajuda pessoas a encontrar veículos. "
    "Extraia da frase do usuário os filtros de busca (marca, modelo, ano mínimo, tipo de combustível, cor, transmissão, categoria, preço máximo). "
    "Sempre que houver múltiplos valores, retorne como lista. "
    "Exemplo: 'Quero um sedan preto automático, Honda ou Toyota, até 60 mil, de 2018 pra frente.' "
    "Retorne: categoria=['Sedan'], cor=['Preto'], transmissao=['Automático'], marca=['Honda','Toyota'], preco=60000, ano=2018. "
    "Se não souber algum filtro, ignore. Sempre normalize os valores conforme exemplos das descrições."
)

def main():
    print("Bem-vindo ao buscador de veículos conversacional!\nDigite sua busca em linguagem natural (ou 'sair' para encerrar):\n")
    while True:
        frase = input("Você: ").strip()
        if frase.lower() in ("sair", "exit", "quit"):
            print("Até logo!")
            break

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": frase}
            ],
            tools=[{"type": "function", "function": function_schema}],  # type: ignore
            tool_choice={"type": "function", "function": {"name": "extrair_filtros_veiculo"}}
        )
        message = response.choices[0].message
        args = "{}"
        if hasattr(message, "tool_calls") and message.tool_calls and hasattr(message.tool_calls[0].function, "arguments"):
            args = message.tool_calls[0].function.arguments
        try:
            filtros = json.loads(args)
        except json.JSONDecodeError:
            filtros = {}

        params = {k: v for k, v in filtros.items() if v}
        resp = requests.get(SERVER_URL, params=params)
        if resp.status_code == 200:
            veiculos = resp.json()
        else:
            print("Erro ao buscar veículos:", resp.text)
            veiculos = []

        if not veiculos:
            print("\nNenhum veículo encontrado com esses filtros. Tente ser menos restritivo.\n")
            continue

        for v in veiculos:
            print("-" * 60)
            print(f"Marca:        {v['marca']}")
            print(f"Modelo:       {v['modelo']}")
            print(f"Ano:          {v['ano']}")
            print(f"Cor:          {v['cor']}")
            print(f"Combustível:  {v['tipo_combustivel']}")
            print(f"Transmissão:  {v['transmissao']}")
            print(f"Categoria:    {v['categoria']}")
            print(f"Preço:        R$ {v['preco']:.2f}")
        print("-" * 60)
        print(f"\nTotal encontrado: {len(veiculos)}\n")

if __name__ == "__main__":
    main() 