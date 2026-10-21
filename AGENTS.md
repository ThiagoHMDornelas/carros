# AGENTS.md — carros

Catálogo e venda de carros com descrição do veículo gerada por IA. Django 5.2.4 (templates + CBV, sem DRF), Python 3.12, SQLite padrão, com clientes opcionais de IA (OpenAI, Gemini, Mistral) e deploy uWSGI/Docker.

## Contexto em camadas
`SOUL.md` (regras globais do agente) → `AGENTS.md` da pasta da linguagem (regras comuns) → este arquivo (particularidades do projeto). Em conflito, vale o mais específico (este arquivo), exceto em regras de segurança/global.

## Arquitetura

- **Módulo de settings**: `app.settings` — o pacote de configuração do Django chama-se `app`, não `carros`. `ROOT_URLCONF` é `app.urls` e todas as URLs ficam centralizadas em `app/urls.py` (os apps não têm `urls.py` próprios).
- **Sem API REST**: este projeto é apenas full-stack Django. O pacote `api_ia/` não é um app Django e não é registrado no `settings.py` — é um módulo standalone com um cliente por provedor (`openai_client.py`, `gemini_client.py`, `mistralai_client.py`), cada um lendo a própria chave do `.env` via `os.getenv` e levantando `ValueError` se a chave não existir.
- **Multa-database via router**: `DATABASE_ROUTERS = ['app.db_routers.SimpleRouter']`. O `SimpleRouter` direciona leitura/escrita/migração para o banco escolhido em `ACTIVE_DB` (`default` = SQLite, `postgresql` = bloco `POSTGRES_*`). A flag `ACTIVE_DB` é lida no settings com `python-decouple`.
- **Ambiente**: `python-decouple` (settings) + `python-dotenv` (clientes de IA); as chaves ficam em `.env` (modelo em `.env.example`), incluindo `SECRET_KEY` e as chaves de IA.

### Apps

| App/pasta | Finalidade | Particularidades |
|---|---|---|
| `app/` | Config do projeto, URLs raiz (todas), `db_routers.py` | Pacote chama-se `app`, não `carros` |
| `cars/` | Catálogo de carros: `Brand`, `Car`, `CarInventory` | CBV + decoração com `@method_decorator(login_required)` no `dispatch` |
| `accounts/` | Registro, login e logout de usuários | Views function-based com `UserCreationForm`/`AuthenticationForm`; usa o `User` padrão do Django (sem model próprio) |
| `api_ia/` | Clientes de IA para biografia do carro | Não é app Django; se a chave de IA faltar, o cliente levanta `ValueError` |
| `app/templates/` | Layout base; templates dos apps em `<app>/templates/` | |

## Testes e lint

- Suíte obrigatória antes de entregar: **`python manage.py test`** (runner nativo do Django, `cars/tests.py`).
- Lint com flake8 (config em `.flake8`: ignora E501, exclui `.venv`).
- O CI (`.github/workflows/tests.yml`) roda apenas `python manage.py test` em Python 3.12 a cada push/PR — o flake8 **não** faz parte do CI.

## Banco de dados

- `ACTIVE_DB=default` → SQLite (`db.sqlite3` no projeto).
- `ACTIVE_DB=postgresql` → PostgreSQL via `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`.
- O Docker força `ACTIVE_DB=default`.

## Variáveis de ambiente (.env.example)

`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `ACTIVE_DB`, `POSTGRES_*` (5 variáveis) e as chaves opcionais de IA: `GEMINI_API_KEY`, `OPENAI_API_KEY`, `MISTRAL_API_KEY`. Sem chave de IA, a geração de biografia não funciona (o sinal preenche `bio` com texto padrão).

## Signals

Importados no `ready()` de `cars/apps.py`:
- `pre_save` em `Car`: se `bio` vazia, preenche com texto padrão.
- `post_save`/`post_delete` em `Car`: cria um **novo registro** de `CarInventory` (snapshot com contagem de carros e soma de `value` — o inventário é histórico de snapshots, não um contador único atualizado).

## Docker

- Serviço único `web` (imagem `python:3.12-slim`), porta `8000:8000`, `env_file: .env`.
- O container roda `migrate && runserver 0.0.0.0:8000` e sobrescreve `SECRET_KEY`/`DEBUG`/`ACTIVE_DB` do `.env`.
- Não há serviço de banco no compose: o container usa SQLite dentro do container.

## Convenções

- Secrets **sempre** em `.env` (nunca hardcode); mantenha o `.env.example` atualizado e o `.env` fora do versionamento.
- Migrações que apagam ou tornam campo obrigatório sem `default` precisam de aviso antes de rodar em produção.
- Mensagens de UI/validação em português do Brasil, revisadas (acentuação e concordância).
- Não commitar/pushar por conta própria: as alterações ficam prontas para o usuário revisar e commitar.
- Preservar encoding dos arquivos ao editar (não converter ANSI ↔ UTF-8 sem pedido explícito).
