# Desafio Técnico – C2S

## Visão Geral

Projeto para busca de veículos com agente conversacional, usando Python, FastAPI, SQLAlchemy, OpenAI.

- **Agente virtual realmente conversacional**: entende frases em linguagem natural e extrai filtros com LLM (OpenAI).
- **API robusta e flexível**: aceita múltiplos filtros, busca case-insensitive, suporta múltiplos valores (ex: Honda ou Toyota).
- **Banco populado com dados realistas**: 100 veículos variados, cobrindo diferentes marcas, modelos e categorias.

## Estrutura do Projeto

```
C2S/
│
├── client/           # Cliente MCP (agente virtual via terminal)
├── server/           # Servidor MCP (API para consulta banco)
├── db/               # Modelos e scripts de banco de dados
├── tests/            # Testes automatizados
├── README.md
└── requirements.txt
```

## Como rodar o projeto

1. **Clone o repositório e entre na pasta**
2. **Crie e ative a venv**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Instale as dependências**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Configure a chave da OpenAI**
   - Crie um arquivo `.env` na raiz do projeto com o conteúdo:
     ```
     OPENAI_API_KEY=sua-chave-aqui
     ```
5. **Popule o banco de dados**
   ```bash
   python3 db/populate.py
   ```
6. **Inicie o servidor FastAPI**
   ```bash
   uvicorn server.server:app --reload
   ```
7. **Rode o agente virtual no terminal**
   ```bash
   python3 client/client.py
   ```

## Exemplos de uso

- "Quero um sedan preto automático, Honda ou Toyota, até 60 mil, de 2018 pra frente."
- "Procuro um SUV branco, flex, até 80 mil."
- "Busco um hatch manual, qualquer cor, até 40 mil."

## Testes Automatizados

Para rodar os testes:
```bash
pytest tests/test_api.py
```
Os testes cobrem busca geral e busca com filtro simples, por marca e categoria.

## Decisões Técnicas

- **Conversacional de verdade**: O agente entende frases livres, não menus rígidos.
- **Function calling OpenAI**: Garante extração robusta e estruturada dos filtros.
- **Normalização de dados**: Corrige possíveis ambiguidades da LLM (ex: sedan como categoria).
- **Flexibilidade**: Backend aceita múltiplos valores para filtros, busca insensível a maiúsculas/minúsculas.

---
