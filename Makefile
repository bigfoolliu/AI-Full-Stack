APP_DIR := ai-knowledge-base
FRONTEND_DIR := $(APP_DIR)/frontend
BACKEND_DIR := $(APP_DIR)/backend

.PHONY: help frontend-dev frontend-build frontend-preview backend-dev backend-test qdrant-up qdrant-down check

help:
	@echo "Available targets:"
	@echo "  make frontend-dev     Start Vite dev server"
	@echo "  make frontend-build   Build frontend"
	@echo "  make frontend-preview Preview frontend production build"
	@echo "  make backend-dev      Start FastAPI with reload"
	@echo "  make backend-test     Run backend validation scripts"
	@echo "  make qdrant-up        Start Qdrant via docker-compose"
	@echo "  make qdrant-down      Stop Qdrant"
	@echo "  make check            Run default verification"

frontend-dev:
	cd $(FRONTEND_DIR) && npm run dev

frontend-build:
	cd $(FRONTEND_DIR) && npm run build

frontend-preview:
	cd $(FRONTEND_DIR) && npm run preview

backend-dev:
	cd $(BACKEND_DIR) && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

backend-test:
	cd $(BACKEND_DIR) && env -u ALL_PROXY -u all_proxy -u HTTP_PROXY -u http_proxy -u HTTPS_PROXY -u https_proxy uv run python scripts/test_parser.py
	cd $(BACKEND_DIR) && env -u ALL_PROXY -u all_proxy -u HTTP_PROXY -u http_proxy -u HTTPS_PROXY -u https_proxy uv run python scripts/test_process.py
	cd $(BACKEND_DIR) && env -u ALL_PROXY -u all_proxy -u HTTP_PROXY -u http_proxy -u HTTPS_PROXY -u https_proxy uv run python scripts/test_semantic_search.py
	cd $(BACKEND_DIR) && env -u ALL_PROXY -u all_proxy -u HTTP_PROXY -u http_proxy -u HTTPS_PROXY -u https_proxy uv run python scripts/test_chat.py
	cd $(BACKEND_DIR) && env -u ALL_PROXY -u all_proxy -u HTTP_PROXY -u http_proxy -u HTTPS_PROXY -u https_proxy uv run python scripts/test_sessions.py

qdrant-up:
	cd $(APP_DIR) && docker-compose up -d

qdrant-down:
	cd $(APP_DIR) && docker-compose down

check: frontend-build backend-test
