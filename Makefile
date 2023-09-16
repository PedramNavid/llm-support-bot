.PHONY: install backend frontend
install:
	pip install -e backend/.
	cd frontend && npm install

dev-api:
	uvicorn main:app --reload --port 3000 --host 0.0.0.0 --workers 1 --app-dir=./backend

api:
	uvicorn main:app --port 80 --host 0.0.0.0 --workers 1 --app-dir=./backend
serve:
	cd frontend && gatsby serve
