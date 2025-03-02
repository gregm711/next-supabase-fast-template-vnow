include ../.env.local

ngrok:
	ngrok http 8000 --domain=${NGROK_STATIC_URL}

clean:
	docker-compose down
	pkill -f ngrok || true

build:
	docker compose build --no-cache api

up:
	docker compose up

up_hidden:
	docker compose up -d

down:
	docker compose downmake

run: build up

verify_types:
	@$(VENV_ACTIVATE) $(SHELL_CMD_SEP) \
	mypy app
