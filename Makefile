.PHONY: up down logs test lint shell-api shell-ui wipe

# ── Docker Compose ───────────────────────────────────────────────────────────
up:          ## Build images and start all services
	docker compose up --build

up-d:        ## Start in background
	docker compose up --build -d

down:        ## Stop and remove containers (data volume preserved)
	docker compose down

wipe:        ## Stop containers AND delete the data volume (wipes SQLite DB)
	docker compose down -v

logs:        ## Tail logs for all services
	docker compose logs -f

logs-api:    ## Tail API logs only
	docker compose logs -f api

logs-ui:     ## Tail UI logs only
	docker compose logs -f ui

shell-api:   ## Open a bash shell in the api container
	docker compose exec api bash

shell-ui:    ## Open a bash shell in the ui container
	docker compose exec ui bash

# ── Local development (no Docker) ────────────────────────────────────────────
install:     ## Create venv and install all dependencies
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

run-api:     ## Run FastAPI locally (PYTHONPATH set)
	PYTHONPATH=. .venv/bin/uvicorn src.api.main:app --reload

run-ui:      ## Run Streamlit locally
	PYTHONPATH=. .venv/bin/streamlit run src/ui/app.py

test:        ## Run full test suite (76 tests)
	PYTHONPATH=. .venv/bin/pytest tests/ -v

test-q:      ## Run tests (quiet)
	PYTHONPATH=. .venv/bin/pytest tests/ -q

help:        ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'
