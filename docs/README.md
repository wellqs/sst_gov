# Documentação rápida do SST_GOV

## Stack e módulos
- **Backend**: Django 5 + PostgreSQL (Docker Compose expõe web em 8002 e DB em 5433).
- **Apps**: core (gestão), acidentes (S-2210/CAT), epi (catálogo/entregas), exames (S-2220), relatorios. Inspeções/treinamentos ainda em construção.
- **Chat IA**: endpoint `/api/chat` usa OPENAI_API_KEY do `.env`.

## Subir ambiente local
```bash
docker compose up -d          # sobe Postgres e web (migrations já são executadas na subida)
docker compose exec -T web python manage.py createsuperuser  # criar admin
```
Acesse `http://localhost:8002/` ou `/login`.

## Variáveis de ambiente (.env)
- `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST=db`, `POSTGRES_PORT=5433`
- `OPENAI_API_KEY` (não versionar a chave real)

## Comandos de importação e dados
Executar sempre no contêiner web (ajuste o caminho se usar outro CSV):
```bash
docker compose exec -T web python manage.py importar_epis --arquivo /app/data/epis.csv
docker compose exec -T web python manage.py importar_cargos --arquivo /app/data/cargos_hospital.csv
docker compose exec -T web python manage.py importar_setores --arquivo /app/data/setores.csv
docker compose exec -T web python manage.py importar_servidores --arquivo /app/data/servidores_ht.csv
docker compose exec -T web python manage.py carregar_dados_demo  # carrega dados de exemplo
```
Formatos (UTF-8):
- `epis.csv`: `Nome;CA;Validade CA;Categoria;Tamanho` (usa `;`).
- `cargos_hospital.csv`: `Titulo,CBO,Descricao,Ativo`.
- `setores.csv`: `Unidade,Nome,Codigo,Descricao,Ativa`.
- `servidores_ht.csv`: campos conforme comando `importar_servidores` (CPF, matrícula, unidade, setor, cargo etc.).

## URLs úteis
- Home: `/` (cards dos módulos)
- Login/Logout: `/login`, `/logout`
- Gestão: `/gestao/` (servidores, unidades, setores, cargos)
- EPI: `/epi/catalogo/` (catálogo), `/epi/listar/` (entregas)
- Acidentes: `/acidentes/` (dashboard), `/acidentes/listar/`
- Exames: `/exames/`
- Relatórios: `/relatorios/` (+ saúde/segurança)
- Healthcheck: `/health/`

## Boas práticas
- Nunca versionar `.env` com chaves reais; usar `.env.example` como referência.
- Para produção: ajustar `ALLOWED_HOSTS`, HTTPS/CSRF, coletar estáticos (`collectstatic`) e usar servidor WSGI/ASGI adequado.
- Padrão de commits em português e descritivos.
