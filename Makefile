# Makefile para comandos rápidos do projeto Django com Docker Compose

.PHONY: help build up down recreate migrate makemigrations shell logs test

help:
	@echo "Uso: make <target>"
	@echo "  build        Builda as imagens Docker"
	@echo "  up           Sobe os serviços (web + db)"
	@echo "  up-debug     Sobe o web com stdin/tty pra debug (breakpoint/pdb)"
	@echo "  down         Para os serviços"
	@echo "  recreate     Rebuild e sobe os serviços"
	@echo "  migrate      Executa as migrations Django"
	@echo "  makemigrations Cria novas migrations Django"
	@echo "  shell        Abre shell Django no container web"
	@echo "  logs         Exibe logs do Docker Compose"
	@echo "  test         Roda os testes Django"

build:
	docker compose build

up:
	docker compose up

debug:
	docker compose up -d db
	docker compose run --rm --service-ports web python -m debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000

down:
	docker compose down

recreate: down build up

migrate:
	docker compose run --rm web python manage.py migrate

makemigrations:
	docker compose run --rm web python manage.py makemigrations

shell:
	docker compose run --rm web python manage.py shell

logs:
	docker compose logs -f

test:
	docker compose run --rm web python manage.py test
