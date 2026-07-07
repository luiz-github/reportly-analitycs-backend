# Backend Docker Setup

Use este projeto com Docker Compose.

## Comandos

- `make build` - builda as imagens
- `make up` - sobe os serviços
- `make down` - para os serviços
- `make migrate` - aplica migrations
- `make makemigrations` - cria migrations
- `make shell` - abre shell Django
- `make logs` - monitora os logs
- `make test` - roda testes

## Variáveis de ambiente

Definidas em `.env`

- `DEBUG`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
