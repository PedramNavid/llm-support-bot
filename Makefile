.PHONY: install backend frontend
install:
	pip install -e backend/.
	cd frontend && npm install && npm build

dev-api:
	uvicorn main:app --reload --port 3000 --host 0.0.0.0 --workers 1 --app-dir=./backend/llm_support_bot

dev-web:
	cd frontend && npm run dev -- --port 8000

api:
	uvicorn main:app --port 80 --host 0.0.0.0 --app-dir=./backend/llm_support_bot
serve:
	cd frontend && gatsby serve
