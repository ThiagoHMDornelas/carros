# AGENTS.md — carros

> Gerado automaticamente na clonagem para a VPS (21/10/2026). **Revisar**: ajuste o que não bater com a realidade do projeto.

## Visão geral
Aplicação **Django** para catálogo e venda de carros, com geração de biografia do veículo por IA.

**Stack:** Django 5.2.4 · Python 3.12 · SQLite (padrão) ou PostgreSQL · Pillow · OpenAI / Gemini / Mistral · uWSGI · Docker

## Contexto em camadas
`~/.hermes/SOUL.md` (regras globais) → `~/projetos/python/AGENTS.md` (regras da linguagem) → este arquivo (particularidades do projeto).
Em conflito, vale o mais específico (este arquivo), exceto em regras de segurança/global.

## Estrutura
- `carros/` — projeto Django (`app/settings.py` é o settings)
- `cars/`, `accounts/` — apps (catálogo de carros, contas de usuário)
- `api_ia/` — integração com os provedores de IA
- `carros_uwsgi.ini`, `uwsgi_params` — deploy com uWSGI
- `docker-compose.yml`, `Dockerfile` (porta 8000)

## Como rodar
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements_dev.txt
cp .env.example .env          # ajustar SECRET_KEY e chaves de IA
python manage.py migrate
python manage.py runserver
```

## Testes e lint
```bash
python manage.py test
flake8
```
(Mesmos comandos usados no CI em `.github/workflows/tests.yml`.)

## Banco de dados
`ACTIVE_DB=default` (SQLite) ou `ACTIVE_DB=postgresql` + bloco `POSTGRES_*` do `.env.example`.

## Variáveis de ambiente
`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `ACTIVE_DB`, `POSTGRES_*`, e as chaves opcionais de IA (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `MISTRAL_API_KEY`). Sem chave de IA, a biografia automática fica indisponível.

## Convenções
- Secrets **sempre** em `.env` (nunca hardcode); mantenha o `.env.example` atualizado e o `.env` fora do versionamento.
- Migrações que apagam ou tornam campo obrigatório sem `default` precisam de aviso antes de rodar em produção.
- Mensagens de UI/validação em português do Brasil, revisadas (acentuação e concordância).
- Não commitar/pushar por conta própria: as alterações ficam prontas para o usuário revisar e commitar.
- Preservar encoding dos arquivos ao editar (não converter ANSI ↔ UTF-8 sem pedido explícito).
