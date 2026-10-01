# Carros

![Testes](https://github.com/ThiagoHMDornelas/carros/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Django](https://img.shields.io/badge/django-5.2-092E20)

Aplicação web para catálogo e venda de carros, desenvolvida com Django. Permite listar e gerenciar carros e marcas, com autenticação de usuários, inventário automático e geração da descrição dos veículos com IA (OpenAI, Gemini ou MistralAI).

## Sumário

- [Visão geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Instalação e execução](#instalação-e-execução)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Bancos de dados](#bancos-de-dados)
- [Executar com Docker](#executar-com-docker)
- [Testes](#testes)
- [Principais rotas](#principais-rotas)
- [Integração com IA](#integração-com-ia)
- [Painel administrativo](#painel-administrativo)

## Visão geral

O **Carros** é uma aplicação web de catálogo e venda de veículos construída com Django (templates e Class-Based Views). Visitantes podem consultar a lista e os detalhes dos carros; usuários autenticados podem cadastrar, alterar e remover carros. As marcas são gerenciadas por administradores no painel administrativo. O inventário é atualizado automaticamente a cada alteração e cada carro pode ter sua descrição gerada por IA.

## Funcionalidades

- Listagem de carros com busca por modelo
- Detalhe do carro
- Cadastro, alteração e exclusão de carros (requer login)
- Gerenciamento de marcas pelo painel administrativo (administradores)
- Inventário atualizado automaticamente via signals (quantidade e valor total)
- Registro, login e logout de usuários
- Geração da descrição do carro com IA (OpenAI, Gemini ou MistralAI)
- Painel administrativo do Django

## Tecnologias

- Python
- Django 5.2
- python-decouple (variáveis de ambiente)
- python-dotenv
- Pillow (upload de imagens)
- SQLite e PostgreSQL
- OpenAI, Google Gemini e MistralAI (integrações opcionais)
- Docker e Docker Compose
- flake8 (desenvolvimento)
- GitHub Actions (CI)

## Estrutura do projeto

```
carros/
├── app/                # configurações do projeto (settings, urls, db_routers)
├── accounts/           # autenticação (registro, login, logout)
├── cars/               # app de carros e marcas (+ signals de inventário)
├── api_ia/             # clientes de IA (OpenAI, Gemini, MistralAI)
├── media/              # uploads (imagens dos carros)
├── .github/workflows/  # pipeline de CI (GitHub Actions)
├── Dockerfile
├── docker-compose.yml
├── .env.example        # exemplo de variáveis de ambiente
├── manage.py
├── requirements.txt
└── requirements_dev.txt
```

## Instalação e execução

Pré-requisitos:

- Python 3.11 ou superior instalado

Crie um ambiente virtual:

    python -m venv .venv

No Windows, ative o ambiente virtual:

    .venv\Scripts\activate

No Linux ou macOS, ative o ambiente virtual:

    source .venv/bin/activate

Instale as dependências:

    pip install -r requirements.txt

Opcionalmente, para desenvolvimento (lint), instale também:

    pip install -r requirements_dev.txt

Execute as migrações:

    python manage.py migrate

Crie um usuário administrador:

    python manage.py createsuperuser

Inicie o servidor:

    python manage.py runserver

A aplicação estará disponível em:

    http://127.0.0.1:8000/

## Variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e ajuste os valores:

    # Django
    SECRET_KEY=troque-por-uma-chave-secreta
    DEBUG=True
    ALLOWED_HOSTS=*

    # Banco de dados ativo: default (SQLite) ou postgresql
    ACTIVE_DB=default

    # PostgreSQL (usado quando ACTIVE_DB=postgresql)
    POSTGRES_DB=carros
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432

    # Chaves de IA (opcionais, usadas para gerar a descrição dos carros)
    GEMINI_API_KEY=
    OPENAI_API_KEY=
    MISTRAL_API_KEY=

## Bancos de dados

O projeto pode rodar com dois bancos, alternados pela variável `ACTIVE_DB` no `.env`:

- `default` → SQLite (`db.sqlite3`)
- `postgresql` → PostgreSQL (servidor local na porta 5432)

O roteamento entre os bancos é feito pelo `SimpleRouter` em `app/db_routers.py`.

## Executar com Docker

Com o Docker e o Docker Compose instalados, é possível subir a aplicação sem configurar o ambiente Python manualmente:

    docker compose up --build

A aplicação estará disponível em:

    http://localhost:8000/

Para parar e remover os containers:

    docker compose down

As migrações são aplicadas automaticamente na inicialização. O banco SQLite é criado dentro do container, então os dados não persistem após um `docker compose down`.

## Testes

A suíte de testes cobre models, formulários, views e os signals de inventário. Execute:

    python manage.py test

A suíte também roda automaticamente a cada `push` e `pull request` via **GitHub Actions** (`.github/workflows/tests.yml`), e o resultado é exibido no badge no topo deste README.

## Principais rotas

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Redireciona para a lista de carros |
| GET | `/carros/` | Lista de carros (pública) |
| GET | `/carro/<id>` | Detalhe do carro |
| GET/POST | `/novo_carro/` | Cadastro de carro (requer login) |
| GET/POST | `/carro/<id>/alterar` | Alterar carro (requer login) |
| GET/POST | `/carro/<id>/deletar` | Excluir carro (requer login) |
| GET/POST | `/registro/` | Cadastro de usuário |
| GET/POST | `/login/` | Login |
| GET | `/logout/` | Logout |
| GET | `/admin/` | Painel administrativo |

## Integração com IA

O app `api_ia` contém clientes para OpenAI, Google Gemini e MistralAI que geram uma descrição de venda a partir do modelo, marca e ano do carro. Basta informar a chave correspondente no `.env` e chamar a função desejada; a integração já está preparada para ser ativada no `cars/signals.py`.

## Painel administrativo

Acesse `/admin/` com o superusuário criado. Carros e marcas ficam disponíveis para gerenciamento, com busca por modelo e por marca. As marcas são cadastradas por aqui — como cada carro está vinculado a uma marca, é preciso ter ao menos uma marca cadastrada antes de criar um carro.
