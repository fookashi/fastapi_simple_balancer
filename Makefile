.PHONY: up down logs migrate migrate-down clean

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose run --rm migrator up

migrate-down:
	docker compose run --rm migrator down

clean:
	docker compose down -v --remove-orphans
