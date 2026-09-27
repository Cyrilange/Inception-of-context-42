.PHONY: up down build logs ps shell restart clean

up:
	docker compose up -d --build

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

ps:
	docker compose ps

shell:
	docker compose exec ioc /bin/bash

restart:
	docker compose restart

clean:
	docker compose down -v