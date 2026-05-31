PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn

.PHONY: install run dev up down

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	@test -d $(VENV) || $(MAKE) install
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

dev: up run

up:
	docker compose up -d

down:
	docker compose down
